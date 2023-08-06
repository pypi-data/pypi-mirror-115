import sys
import time

from rq import Connection, Queue, Worker
from rq.defaults import DEFAULT_JOB_MONITORING_INTERVAL
from rq.job import Job

from csengine.extentions.rq.services import EventService
from csengine.utils.package import get_packages


class WorkerJob(Job):
    worker = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._before_time = None
        self._after_time = None

    def run_pre_processing(self):
        self.meta['packages'] = get_packages()
        self.save_meta()
        self._before_time = time.perf_counter()
        self._after_time = time.perf_counter()
        self.send_notification('JOB_STARTED')

    def run_post_processing(self, result):
        self._after_time = time.perf_counter()
        duration = self._after_time - self._before_time
        self.send_notification('JOB_FINISHED', {'duration': duration})

    def handle_exception(self, e):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        self.send_notification('JOB_FAILED', {'exc_type': str(exc_type)})

    def send_notification(self, event, body=None):
        body = body or {}
        self.worker.send_notification(event, dict(body, job=self.id))

    def _execute(self):
        try:
            self.run_pre_processing()
            result = super()._execute()
            self.run_post_processing(result)
            return result
        except Exception as e:
            self.handle_exception(e)
            raise e from None


class RQWorker(Worker):

    def __init__(self, *args, pre_processing_handlers=None, post_processing_handlers=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._pre_processing_handlers = pre_processing_handlers or []
        self._post_processing_handlers = post_processing_handlers or []

    def execute_job(self, job, queue):
        for handler in self._pre_processing_handlers:
            handler(job)
        super().execute_job(job, queue)
        for handler in self._post_processing_handlers:
            handler(job)


class App:
    job_class = WorkerJob
    worker_class = RQWorker
    serializer = None
    event_service_class = EventService

    def __init__(self, redis_conn, queues, job_monitoring_interval=None):
        super().__init__()
        self._worker = None
        self._queues = queues
        self._redis_conn = redis_conn
        self._job_monitoring_interval = job_monitoring_interval or DEFAULT_JOB_MONITORING_INTERVAL
        self._event_service = self.event_service_class(self._redis_conn)

    def run(self, job_class=None):
        with Connection(self._redis_conn):
            job_class = job_class or self.job_class
            job_class.worker = self
            self._worker = self.worker_class(list(map(Queue, self._queues)),
                                             log_job_description=False,
                                             job_class=job_class,
                                             pre_processing_handlers=[self.handle_pre_processing],
                                             post_processing_handlers=[self.handle_post_processing],
                                             exception_handlers=[self.log_exception],
                                             job_monitoring_interval=self._job_monitoring_interval,
                                             serializer=self.serializer)
            self._worker.work()

    def send_notification(self, event, body):
        if self._event_service:
            self._event_service.send_notification(event, dict(body, worker=self._worker.name))

    def handle_pre_processing(self, job):
        pass

    def handle_post_processing(self, job):
        pass

    def log_exception(self, job, exc_type, exc_value, traceback):
        job.meta['exception'] = str(exc_type)
        job.save_meta()

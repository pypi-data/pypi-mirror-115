import json
import logging
import threading
import time

import redis
from rq import Queue
from rq.job import Job, cancel_job
from rq.exceptions import NoSuchJobError

from csengine.observer import Event
from csengine.service import Service

logger = logging.getLogger(__name__)


class EventService(Service):
    event_channel = 'rq:events'

    def __init__(self, redis_conn):
        super().__init__()
        self._redis_conn = redis_conn
        self._handlers = []

    def send_notification(self, event, body):
        self._redis_conn.publish(self.event_channel, json.dumps({'event': event, 'body': body}))

    def subscribe(self, handler):
        self._handlers.append(handler)

    def fire(self, event, body):
        for handler in self._handlers:
            handler(event, body)

    def run(self):
        thread = threading.Thread(target=self.listen)
        thread.daemon = True
        thread.start()

    def listen(self):
        pubsub = self._redis_conn.pubsub()
        pubsub.psubscribe(f'{self.event_channel}*')

        logger.info('Starting event loop')
        while True:
            message = pubsub.get_message()
            if message:
                logger.debug(message)
                if message['type'] == 'pmessage':
                    notification = json.loads(message['data'])
                    try:
                        self.fire(notification['event'], notification['body'])
                    except Exception as e:
                        logger.exception(e)
            else:
                time.sleep(0.01)


class TaskService(Service):
    queue_name_default = 'tasks'
    result_ttl_default = 60 * 60 * 24
    failure_ttl_default = 60 * 60 * 24
    timeout_default = 300
    tasks_package = 'tasks'
    serializer = None

    def __init__(self, url, queue_name=None, result_ttl=None, timeout=None, failure_ttl=None,
                 name=None):
        super().__init__(name)
        self._queues = {}
        self._url = url
        self._redis_conn = redis.from_url(url)
        self._queue_name = queue_name or self.queue_name_default
        self._result_ttl = result_ttl or self.result_ttl_default
        self._timeout = timeout or self.timeout_default
        self._failure_ttl = failure_ttl or self.failure_ttl_default
        self._default_queue = Queue(self._queue_name, connection=self._redis_conn,
                                    serializer=self.serializer)

    async def create(self, func, args=None, kwargs=None, timeout=None, result_ttl=None,
                     queue_name=None, failure_ttl=None, max_retries=3, meta=None):
        timeout = timeout or self._timeout
        result_ttl = result_ttl or self._result_ttl
        failure_ttl = failure_ttl or self._failure_ttl
        queue = Queue(queue_name, connection=self._redis_conn, serializer=self.serializer) \
            if queue_name else self._default_queue
        full_func = f'{self.tasks_package}.{func}' if self.tasks_package else func
        meta = meta or {}
        meta.update({'max_retries': max_retries, 'retry_counter': max_retries})
        job = queue.enqueue(full_func, args=args, kwargs=kwargs, job_timeout=timeout,
                            result_ttl=result_ttl, failure_ttl=failure_ttl, meta=meta)
        event_payload = {
            'name': func,
            'args': args,
            'kwargs': kwargs,
            'options': {
                'timeout': timeout,
                'result_ttl': result_ttl,
            },
            'meta': meta
        }
        await self.app.notify(Event('TASK_CREATED', event_payload))
        return job

    async def get(self, task_id):
        try:
            return Job.fetch(task_id, connection=self._redis_conn)
        except NoSuchJobError:
            return None

    async def delete(self, task_id):
        try:
            job = Job.fetch(task_id, connection=self._redis_conn)
            job.delete(remove_from_queue=True, delete_dependents=True)
        except NoSuchJobError:
            return None

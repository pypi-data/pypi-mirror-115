from functools import wraps

from prometheus_client import Counter, Gauge
from rq import get_current_job


class Metrics:
    JOBS_TOTAL = Counter('worker_jobs_total', 'Worker jobs total count', ['func_name'])
    JOBS_IN_PROGRESS = Gauge('worker_jobs_in_progress_total', 'Worker jobs in progress',
                             ['func_name'])


def metrics(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        job = get_current_job()
        Metrics.JOBS_IN_PROGRESS.labels(func_name=job.func_name).inc()
        job_results = func(*args, **kwargs)
        Metrics.JOBS_IN_PROGRESS.labels(func_name=job.func_name).dec()
        Metrics.JOBS_TOTAL.labels(func_name=job.func_name).inc()
        return job_results

    return wrapper

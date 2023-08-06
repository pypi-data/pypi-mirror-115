import logging

from fastapi import Request

log = logging.getLogger('fastapi_tracing')


async def log_request(request: Request):
    log.debug(await make_request_log(request))


async def make_request_log(request, replace_authorization=True):
    # path_template, is_handled_path = self.get_path_template(request)
    headers = dict(request.headers)
    if replace_authorization:
        headers['authorization'] = '*' * len(headers['authorization'])
    # form = await request.form()  # !!! BUG on FastAPI
    # try:
    #     json = await request.json()
    # except:
    #     json = None
    return f"REQUEST {request}: " \
           f"\n \t {request.method} {request.url} "\
           f"\n \t HEADERS: {headers} "\
           f"\n \t QUERY PARAMS: {request.query_params}"\
           f"\n \t PATH PARAMS: {request.path_params}"\
           f"\n \t CLIENT: {request.client}"

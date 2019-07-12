import json
from pkg.constants.version import SOFTWARE_VERSION
from pkg.utils.logger import REST_LOGGER, LOGDNA_LOGGER
from . import app


IGNORE_REQUESTS_LOGGING = [
    # '/api/v1/...'
]


# noinspection PyUnusedLocal
@app.middleware('response')
async def custom_headers(request, resp):
    resp.headers['Server'] = SOFTWARE_VERSION


@app.middleware('request')
async def log_request(request):
    if request.path not in IGNORE_REQUESTS_LOGGING:
        try:
            body = '\nBODY: ' + request.body.decode('utf-8') if request.body else ''
        except:
            body = '\nBODY: <binary data>'
        user_agent = request.headers['user-agent'] if 'user-agent' in request.headers else ''
        auth = f'\nAUTH: {request.headers["authorization"]}' if 'authorization' in request.headers else ''
        args = f'\nARGS: {str(request.raw_args)}' if request.raw_args else ''
        log_body = f'{auth}{args}{body}'
        log_body = f'{log_body}\n' if log_body else ''
        log = f'{request.method} {request.path} from {request.ip} {user_agent}{log_body}'
        REST_LOGGER.info(log)
        LOGDNA_LOGGER.info(log)


def is_static_content(request):
    path = request.path
    for route in app.static_routes:
        m = route.pattern.match(path)
        if m:
            return True, m.group()
    return False, ''


@app.middleware('response')
async def log_response(request, response):
    if request.path not in IGNORE_REQUESTS_LOGGING:
        static = is_static_content(request)
        if static[0]:
            body = f'<see static file {static[1]}>'
        else:
            if response.content_type == 'application/pdf':
                body = f'PDF {len(response.body)} bytes length'
            else:
                try:
                    body = json.dumps(json.loads(response.body.decode('utf-8')), ensure_ascii=False) if response.body else ''
                except:
                    body = response.body.decode('utf-8') if response.body else ''
        body = f'\nBODY: {body}'
        log = f'RESPONSE {response.status} {response.content_type}:{body}\n'
        REST_LOGGER.info(log)
        LOGDNA_LOGGER.info(log)

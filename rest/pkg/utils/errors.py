import logging
import sys
import traceback
from pkg.constants.error_codes import ERROR_TEXT_MAP
from pkg.constants.logging import REST_LOGGER_NAME
from sanic import response
from sanic.request import Request


def get_raised_error(full: bool = False):
    info = sys.exc_info()
    if info[0] is None and info[1] is None and info[2] is None:
        return
    e = traceback.format_exception(*info)
    if full:
        return '\n'.join(e)
    else:
        return (e[-1:][0]).strip('\n')


def response_error(code: int,
                   message: str = None,
                   status: int = 500,
                   default_logger: str = REST_LOGGER_NAME,
                   log_stacktrace: bool = True,
                   log_error: bool = True):

    msg = message if message else ERROR_TEXT_MAP[code]

    error_json = {'error': {'code': code, 'message': msg}}
    stacktrace_log_msg = ''

    if log_stacktrace:
        error_stacktrace = get_raised_error(True)
        stacktrace_log_msg = f'\n{error_stacktrace}\n' if error_stacktrace else ''

    if log_error:
        logger = logging.getLogger(default_logger)
        log = f'Status: {status}, JSON: {error_json}{stacktrace_log_msg}'
        logger.error(log)

    return response.json(error_json, status=status)


# noinspection PyUnusedLocal
def response_400(request: Request, log_stacktrace: bool = True, log_error: bool = True):
    return response_error(400, f'Request data is invalid', 400, log_stacktrace=log_stacktrace, log_error=log_error)


# noinspection PyUnusedLocal
def response_403(request: Request, log_stacktrace: bool = True, log_error: bool = True):
    return response_error(403, f'Forbidden', 403, log_stacktrace=log_stacktrace, log_error=log_error)


def response_403_short():
    return response_403(None, log_stacktrace=False, log_error=False)


def response_404(request: Request, log_stacktrace: bool = True, log_error: bool = True):
    return response_error(404, f'Requested URL {request.path} not found', 404,
                          log_stacktrace=log_stacktrace, log_error=log_error)

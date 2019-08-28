from pkg.utils.context import get_current_context
from pkg.utils.errors import response_error
from sanic import response
from sanic.request import Request
from typing import Union


def response_ok(result: Union[dict, list, str],
                message: str = None):
    obj = {'result': result}
    if message:
        obj['message'] = message
    return response.json(obj)


def response_400(log_stacktrace: bool = True, log_error: bool = True):
    return response_error(400, f'Request data is invalid', 400, log_stacktrace=log_stacktrace, log_error=log_error)


def response_403(log_stacktrace: bool = True, log_error: bool = True):
    return response_error(403, f'Forbidden', 403, log_stacktrace=log_stacktrace, log_error=log_error)


def response_403_short():
    return response_403(log_stacktrace=False, log_error=False)


def response_404(log_stacktrace: bool = True, log_error: bool = True):
    ctx = get_current_context()
    return response_error(404, f'Requested URL {ctx.request.path} not found', 404,
                          log_stacktrace=log_stacktrace, log_error=log_error)

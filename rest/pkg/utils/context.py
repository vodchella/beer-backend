import inspect

from lib.sanic_peewee import QueryHandlerMixin
from pkg.models import User, Employee
from sanic.request import Request


class ServerContext:
    db: QueryHandlerMixin.aio = None
    request: Request = None
    user: User = None
    employee: Employee = None
    json_body: dict = None

    def __init__(self):
        pass


def get_current_context() -> ServerContext:
    stack = inspect.stack()
    for frame_info in stack:
        frame_vars = frame_info.frame.f_locals
        if frame_vars:
            for _, value in frame_vars.items():
                if callable(value):
                    if hasattr(value, '_app_context'):
                        # noinspection PyProtectedMember
                        ctx = value._app_context
                        if type(ctx) == ServerContext:
                            return ctx

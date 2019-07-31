import inspect


def get_current_context():
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


class ServerContext:
    db = None
    request = None
    user = None
    employee = None

    def __init__(self):
        pass

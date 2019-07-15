import inspect


def get_current_context():
    stack = inspect.stack()
    for frame_info in stack:
        args = frame_info.frame.f_locals
        if args:
            for _, value in args.items():
                if type(value) == ServerContext:
                    return value


class ServerContext:
    request = None
    user = None
    employee = None

    def __init__(self):
        pass

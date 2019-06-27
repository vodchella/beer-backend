from asyncpg.exceptions._base import PostgresError
from functools import wraps
from pkg.constants.error_codes import *
from pkg.constants.logging import DB_LOGGER_NAME
from pkg.utils.errors import response_error, get_raised_error
from pkg.utils.rest import RestContext
from sanic.exceptions import InvalidUsage


def rest_context(func):
    @wraps(func)
    async def wrapped(*positional, **named):
        try:
            ctx = RestContext(positional[0])  # request
            return await func(ctx, **named)
        except PostgresError as e:
            return response_error(ERROR_DATABASE_EXCEPTION, str(e), default_logger=DB_LOGGER_NAME)
        except InvalidUsage as e:
            return response_error(ERROR_JSON_PARSING_EXCEPTION, str(e))
        except:
            return response_error(ERROR_INTERNAL_EXCEPTION, get_raised_error())
    return wrapped


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance

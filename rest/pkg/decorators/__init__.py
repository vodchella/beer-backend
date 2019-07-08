import jwt
import re
from asyncpg.exceptions._base import PostgresError
from functools import wraps
from pkg.constants.error_codes import *
from pkg.constants.logging import DB_LOGGER_NAME
from pkg.services.user_service import UserService
from pkg.utils.errors import response_403_short
from pkg.utils.errors import response_error, get_raised_error
from pkg.utils.jwt import create_secret
from pkg.utils.rest import RestContext
from sanic.exceptions import InvalidUsage


def rest_context(func):
    @wraps(func)
    async def wrapped(*positional, **named):
        try:
            request = positional[0]
            if request.json or len(request.body) == 0:
                context = RestContext(request)
                return await func(context, **named)
        except PostgresError as e:
            return response_error(ERROR_DATABASE_EXCEPTION, str(e), default_logger=DB_LOGGER_NAME)
        except InvalidUsage as e:
            return response_error(ERROR_JSON_PARSING_EXCEPTION, str(e))
        except:
            return response_error(ERROR_INTERNAL_EXCEPTION, get_raised_error())
    return wrapped


REFRESH_TOKENS_REGEXP = re.compile(r'^/api/v1/users/[A-z0-9]+/refresh-tokens$', re.IGNORECASE)


def authenticated_rest_context(func):
    @wraps(func)
    @rest_context
    async def wrapped(*positional, **named):
        context = positional[0]
        headers = context.request.headers
        authorization = headers.get('authorization', None)
        if authorization:
            token = authorization[len('Bearer '):]
            payload = jwt.decode(token, verify=False)
            user_id = payload.get('uid', None)
            if user_id:
                typ = payload.get('typ', None)
                if not ((typ == 'r' and not REFRESH_TOKENS_REGEXP.fullmatch(context.request.path)) or
                        (typ == 'a' and REFRESH_TOKENS_REGEXP.fullmatch(context.request.path))):
                    user = await UserService.find(user_id)
                    if user:
                        secret = create_secret(user)
                        try:
                            jwt.decode(token, secret, algorithms='HS256')
                        except:
                            pass  # Всё равно перейдём к response_403_short()
                        else:
                            context.user = user
                            return await func(context, **named)
        return response_403_short()
    return wrapped


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance

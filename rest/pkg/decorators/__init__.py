import jwt
from asyncpg.exceptions._base import PostgresError
from functools import wraps
from pkg.constants.error_codes import *
from pkg.constants.logging import DB_LOGGER_NAME
from pkg.services.user_service import UserService
from pkg.utils.errors import response_403
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


def authenticated(func):
    @wraps(func)
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
                refresh_tokens_url = f'/api/v1/users/{user_id}/refresh-tokens'
                if (typ == 'r' and context.request.path != refresh_tokens_url) or \
                   (typ == 'a' and context.request.path == refresh_tokens_url):
                    return response_403(context.request, log_stacktrace=False, log_error=False)

                user = await UserService.find(user_id)
                if user:
                    secret = create_secret(user)
                    try:
                        jwt.decode(token, secret, algorithms='HS256')
                    except:
                        return response_403(context.request, log_stacktrace=False, log_error=False)
                    context.user = user
                    return await func(context, **named)
                else:
                    return response_403(context.request)  # Здесь я хочу видеть ошибку, т.к данные в токене неверны
            else:
                return response_403(context.request)  # Здесь я хочу видеть ошибку, т.к данные в токене неверны
        else:
            return response_403(context.request, log_stacktrace=False, log_error=False)
    return wrapped


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance

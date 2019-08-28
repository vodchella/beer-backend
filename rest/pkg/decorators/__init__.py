import jwt
import re
# noinspection PyProtectedMember
from asyncpg.exceptions._base import PostgresError
from functools import wraps
from jwt.exceptions import PyJWTError
from pkg.config import CONFIG
from pkg.constants.error_codes import *
from pkg.constants.logging import DB_LOGGER_NAME
from pkg.rest import app
from pkg.services.employee_service import EmployeeService
from pkg.services.user_service import UserService
from pkg.utils.errors import response_error, get_raised_error
from pkg.utils.jwt import create_secret
from pkg.utils.context import ServerContext, get_current_context
from pkg.utils.responses import response_403_short, response_404
from sanic.exceptions import InvalidUsage


def app_context(func):
    context = ServerContext()
    func._app_context = context

    @wraps(func, assigned=['_app_context'])
    async def wrapped(*positional, **named):
        try:
            request = positional[0]
            if request.json or len(request.body) == 0:
                context.request = request
                context.db = app.db.aio
                async with app.db.async_atomic():
                    return await func(*positional, **named)
        except PostgresError as e:
            return response_error(ERROR_DATABASE_EXCEPTION, str(e), default_logger=DB_LOGGER_NAME)
        except InvalidUsage as e:
            return response_error(ERROR_JSON_PARSING_EXCEPTION, str(e))
        except PyJWTError as e:
            return response_error(ERROR_JWT_EXCEPTION, str(e), 403)
        except:
            return response_error(ERROR_INTERNAL_EXCEPTION, get_raised_error())

    return wrapped


REFRESH_TOKENS_REGEXP = re.compile(r'^/api/v1/users/[A-z0-9]+/refresh-tokens$', re.IGNORECASE)


def authenticated_app_context(func):
    @wraps(func, assigned=['_app_context'])
    @app_context
    async def wrapped(*positional, **named):
        # noinspection PyProtectedMember
        context = wrapped._app_context
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
                            return await func(*positional, **named)
        return response_403_short()
    return wrapped


def employee_app_context(func):
    @wraps(func, assigned=['_app_context'])
    @authenticated_app_context
    async def wrapped(*positional, **named):
        # noinspection PyProtectedMember
        context = wrapped._app_context
        employee = await EmployeeService.find_by_user_id(context.user.user_id)
        if employee and employee.is_active:
            context.employee = employee
            return await func(*positional, **named)
        return response_403_short()
    return wrapped


def json_request(func):
    @wraps(func)
    async def wrapped(*positional, **named):
        ctx = get_current_context()
        body = ctx.request.parsed_json
        if body:
            ctx.json_body = body
            return await func(*positional, **named)
        else:
            return response_error(ERROR_JSON_PARSING_EXCEPTION)
    return wrapped


def application_type(*allowed_types):
    def decorator(func):
        @wraps(func)
        async def wrapped(*positional, **named):
            if CONFIG['app']['type'] in allowed_types:
                return await func(*positional, **named)
            else:
                ctx = get_current_context()
                return response_404()
        return wrapped
    return decorator


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance

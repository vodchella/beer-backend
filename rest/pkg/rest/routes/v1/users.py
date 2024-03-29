from pkg.rest import users
from pkg.constants.error_codes import *
from pkg.constants.regexp import REGEXP_EMAIL, REGEXP_ID
from pkg.decorators import authenticated_app_context, app_context, json_request, application_type
from pkg.services.card_service import CardService
from pkg.services.user_service import UserService
from pkg.utils.context import get_current_context
from pkg.utils.errors import response_error
from pkg.utils.peewee import models_to_json_array
from pkg.utils.responses import response_400, response_404, response_ok
from sanic.request import Request
from sanic_openapi import doc


USER_PATH = f'/<user_id:{REGEXP_ID}>'


# noinspection PyUnusedLocal
@users.post(f'{USER_PATH}/change-password')
@doc.summary('Меняет пароль пользователя')
@authenticated_app_context
@json_request
async def change_password(request: Request, user_id: str):
    ctx = get_current_context()
    old_password = ctx.json_body.get('old', None)
    new_password = ctx.json_body.get('new', None)

    if old_password is None or new_password is None:
        return response_400()

    if ctx.user.user_id != user_id:
        return response_404()

    if not UserService.verify_password(ctx.user, old_password):
        return response_error(ERROR_INCORRECT_PASSWORD)

    await UserService.set_password(ctx.user, new_password)

    return response_ok('ok')


# noinspection PyUnusedLocal
@users.get(f'/<email:{REGEXP_EMAIL}>/login')
@doc.summary('Авторизирует пользователя по email')
@app_context
@json_request
async def login(request: Request, email: str):
    user = await UserService.find_by_email(email)
    if user:
        ctx = get_current_context()
        password = ctx.json_body.get('password', None)
        if password and UserService.verify_password(user, password):
            tokens = await UserService.create_new_tokens(user)
            result = {'user_id': user.user_id, **tokens}
            return response_ok(result)
    return response_error(ERROR_INVALID_USER_OR_PASSWORD)


@users.get(f'{USER_PATH}/login-for-postman')
@doc.summary('Авторизирует пользователя по ID. Доступно только в DEV-окружении')
@app_context
@application_type('dev')
async def login(request: Request, user_id: str):
    user = await UserService.find(user_id)
    if user:
        password = request.args.get('password', None)
        if password and UserService.verify_password(user, password):
            return response_ok(await UserService.create_new_tokens(user))
    return response_error(ERROR_INVALID_USER_OR_PASSWORD)


# noinspection PyUnusedLocal
@users.get(f'{USER_PATH}/refresh-tokens')
@doc.summary('Обновляет токены')
@authenticated_app_context
async def refresh_tokens(request: Request, user_id: str):
    ctx = get_current_context()
    if ctx.user.user_id == user_id:
        return response_ok(await UserService.create_new_tokens(ctx.user))
    return response_404()


# noinspection PyUnusedLocal
@users.get(f'{USER_PATH}/cards')
@doc.summary('Получает список карт пользователя')
@authenticated_app_context
async def list_cards(request: Request, user_id: str):
    ctx = get_current_context()
    if ctx.user.user_id == user_id:
        return response_ok(models_to_json_array(await CardService.find_by_user(user_id)))
    return response_404()

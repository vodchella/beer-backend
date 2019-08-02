from pkg.rest import v1
from pkg.constants.error_codes import *
from pkg.decorators import authenticated_app_context, app_context, json_request
from pkg.services.card_service import CardService
from pkg.services.user_service import UserService
from pkg.utils.context import get_current_context
from pkg.utils.errors import response_error
from pkg.utils.peewee import models_to_json_array
from pkg.utils.responses import response_400, response_404, response_ok
from sanic.request import Request


USER_PATH = '/users/<user_id:[A-z0-9]+>'


@v1.post(f'{USER_PATH}/change-password')
@authenticated_app_context
@json_request
async def change_password(request: Request, user_id: str):
    ctx = get_current_context()
    old_password = ctx.json_body.get('old', None)
    new_password = ctx.json_body.get('new', None)

    if old_password is None or new_password is None:
        return response_400()

    if ctx.user.user_id != user_id:
        return response_404(request)

    if not UserService.verify_password(ctx.user, old_password):
        return response_error(ERROR_INCORRECT_PASSWORD)

    await UserService.set_password(ctx.user, new_password)

    return response_ok('ok')


# noinspection PyUnusedLocal
@v1.get(f'{USER_PATH}/login')
@app_context
@json_request
async def login(request: Request, user_id: str):
    user = await UserService.find(user_id)
    if user:
        ctx = get_current_context()
        password = ctx.json_body.get('password', None)
        if password and UserService.verify_password(user, password):
            return response_ok(await UserService.create_new_tokens(user))
    return response_error(ERROR_INVALID_USER_OR_PASSWORD)


@v1.get(f'{USER_PATH}/login-for-postman')
@app_context
async def login(request: Request, user_id: str):
    user = await UserService.find(user_id)
    if user:
        password = request.raw_args.get('password', None)
        if password and UserService.verify_password(user, password):
            return response_ok(await UserService.create_new_tokens(user))
    return response_error(ERROR_INVALID_USER_OR_PASSWORD)


@v1.get(f'{USER_PATH}/refresh-tokens')
@authenticated_app_context
async def refresh_tokens(request: Request, user_id: str):
    ctx = get_current_context()
    if ctx.user.user_id == user_id:
        return response_ok(await UserService.create_new_tokens(ctx.user))
    return response_404(request)


# noinspection PyUnusedLocal
@v1.get(f'{USER_PATH}/cards')
@authenticated_app_context
async def list_cards(request: Request, user_id: str):
    ctx = get_current_context()
    if ctx.user.user_id == user_id:
        return response_ok(models_to_json_array(await CardService.find_by_user(user_id)))
    return response_404(request)

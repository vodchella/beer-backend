from pkg.rest import v1
from pkg.constants.error_codes import *
from pkg.decorators import authenticated, rest_context
from pkg.services.user_service import UserService
from pkg.utils.errors import response_error, response_400, response_404
from sanic import response


USER_PATH = '/users/<user_id:[A-z0-9]+>'
INVALID_USER_OR_PASSWORD_TEXT = 'Invalid user_id or password'


@v1.post(f'{USER_PATH}/change-password')
@rest_context
@authenticated
async def change_password(context, user_id):
    user = context.user
    body = context.request.json
    if body:
        old_password = body.get('old', None)
        new_password = body.get('new', None)

        if old_password is None or new_password is None:
            return response_400(context.request)

        if user.user_id != user_id:
            return response_404(context.request)

        if not UserService.verify_password(user, old_password):
            return response_error(ERROR_INCORRECT_PASSWORD, 'Invalid old password')

        await UserService.set_password(user, new_password)

        return response.json({'result': 'ok'})
    else:
        return response_error(ERROR_JSON_PARSING_EXCEPTION, 'Invalid JSON')


@v1.get(f'{USER_PATH}/login/password')
@rest_context
async def login(context, user_id):
    user = await UserService.find(user_id)
    if user is None:
        return response_error(ERROR_INVALID_USER_OR_PASSWORD, INVALID_USER_OR_PASSWORD_TEXT)

    body = context.request.json
    if body:
        password = body.get('password', None)

        if password is None:
            return response_400(context.request)

        if not UserService.verify_password(user, password):
            return response_error(ERROR_INVALID_USER_OR_PASSWORD, INVALID_USER_OR_PASSWORD_TEXT)

        return response.json({'result': await UserService.create_new_tokens(user)})
    else:
        return response_error(ERROR_JSON_PARSING_EXCEPTION, 'Invalid JSON')

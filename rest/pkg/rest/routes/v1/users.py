from pkg.rest import v1
from pkg.constants.error_codes import ERROR_INCORRECT_PASSWORD
from pkg.decorators import rest_context
from pkg.services.user_service import UserService
from pkg.utils.errors import response_error, response_400, response_404
from sanic import response


USER_PATH = '/users/<user_id:[A-z0-9]+>'


@v1.post(f'{USER_PATH}/change-password')
@rest_context
async def change_password(context, user_id):
    user = await UserService.find(user_id)
    if user is None:
        return response_404(context.request)

    body = context.request.json
    old_password = body.get('old', None)
    new_password = body.get('new', None)

    if old_password is None or new_password is None:
        return response_400(context.request)

    if not UserService.verify_password(user, old_password):
        return response_error(ERROR_INCORRECT_PASSWORD, 'Passwords don\'t match')

    await UserService.set_password(user, new_password)

    return response.json({'result': 'ok'})


@v1.get(f'{USER_PATH}/login/password')
@rest_context
async def login(context, user_id):
    user = await UserService.find(user_id)
    if user is None:
        return response_404(context.request)

    body = context.request.json
    password = body.get('password', None)

    if password is None:
        return response_400(context.request)

    if not UserService.verify_password(user, password):
        return response_error(ERROR_INCORRECT_PASSWORD, 'Incorrect password')

    return response.json({'result': await UserService.create_new_tokens(user)})

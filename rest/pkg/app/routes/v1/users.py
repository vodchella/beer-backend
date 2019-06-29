from pkg.app import app, v1
from pkg.constants.error_codes import ERROR_PASSWORDS_DONT_MATCH
from pkg.decorators import rest_context
from pkg.models import User
from pkg.utils.argon import *
from pkg.utils.errors import response_400, response_error
from sanic import response


USER_PATH = '/users/<user_id:[A-z0-9]+>'


@v1.post(f'{USER_PATH}/change-password')
@rest_context
async def ping(context, user_id):
    body = context.request.json
    old_password = body.get('old', None)
    new_password = body.get('new', None)

    if old_password is None or new_password is None:
        return response_400(context.request)

    user = await app.db.aio.get(User, User.user_id == user_id)

    try:
        verify_hash(user.password, old_password)
    except:
        return response_error(ERROR_PASSWORDS_DONT_MATCH, 'Passwords don\'t match')

    await app.db.aio.update(User.update(password=hash_password(new_password)).where(User.user_id == user_id))

    return response.json({'result': "ok"})

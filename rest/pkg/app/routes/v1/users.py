from pkg.app import app, v1
from pkg.constants.error_codes import ERROR_PASSWORDS_DONT_MATCH
from pkg.decorators import rest_context
from pkg.models import User
from pkg.utils.argon import verify_hash
from pkg.utils.errors import response_400, response_error
from pkg.utils.peewee import fetch_one
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

    db_result = await app.db.aio.select(User.select().where(User.user_id == user_id))
    user = fetch_one(db_result)

    try:
        verify_hash(user.password, old_password)
    except:
        return response_error(ERROR_PASSWORDS_DONT_MATCH, 'Passwords don\'t match')

    return response.json({'user_id': user_id})

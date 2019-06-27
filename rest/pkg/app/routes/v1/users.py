from pkg.app import v1
from pkg.utils.errors import response_400
from pkg.decorators import rest_context
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
    return response.json({'user_id': user_id})

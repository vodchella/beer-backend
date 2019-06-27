from pkg.app import v1
from pkg.decorators import rest_context
from sanic import response


@v1.post('/users/<user_id:[A-z0-9]+>/change-password')
@rest_context
async def ping(context, user_id):
    return response.json({'user_id': user_id})

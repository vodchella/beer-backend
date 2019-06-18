from pkg.app import v1
from pkg.constants.version import SERVER_VERSION_FULL
from pkg.decorators import handle_exceptions, rest_context
from sanic import response


@v1.get('/ping')
@handle_exceptions
@rest_context
async def ping(context):
    return response.json({'version': SERVER_VERSION_FULL})

from pkg.constants.version import SERVER_VERSION
from pkg.decorators import handle_exceptions
from sanic import response
from . import app, v1


@app.get('/')
@v1.get('/ping')
@handle_exceptions
async def ping(request):
    return response.json({'version': SERVER_VERSION})

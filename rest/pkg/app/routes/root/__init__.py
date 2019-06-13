from pkg.app import app
from pkg.constants.version import SOFTWARE_VERSION
from pkg.decorators import handle_exceptions
from sanic import response


@app.get('/')
@handle_exceptions
async def ping(request):
    return response.json({'software': SOFTWARE_VERSION})

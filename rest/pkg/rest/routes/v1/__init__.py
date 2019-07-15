from pkg.constants.version import SERVER_VERSION_FULL
from pkg.decorators import app_context
from pkg.rest import v1
from pkg.utils.dynamic_import import dynamic_import
from sanic import response


dynamic_import('./pkg/rest/routes/v1',
               'pkg.rest.routes.v1',
               '... loading routes:',
               '...... %s route loaded')


# noinspection PyUnusedLocal
@v1.get('/ping')
@app_context
async def ping(context):
    return response.json({'version': SERVER_VERSION_FULL})

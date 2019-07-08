import importlib
import os
from glob import glob
from pkg.rest import v1
from pkg.constants.version import SERVER_VERSION_FULL
from pkg.decorators import rest_context
from pkg.utils.logger import DEFAULT_LOGGER
from sanic import response


DEFAULT_LOGGER.info(f'... loading routes:')
for md in [os.path.basename(x)[:-3] for x in glob('./pkg/rest/routes/v1/*.py') if x[-11:] != '__init__.py']:
    importlib.import_module(f'pkg.rest.routes.v1.{md}')
    DEFAULT_LOGGER.info(f'...... {md} route loaded')


@v1.get('/ping')
@rest_context
async def ping(context):
    return response.json({'version': SERVER_VERSION_FULL})

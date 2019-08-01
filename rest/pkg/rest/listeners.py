from pkg.utils.logger import REST_LOGGER
from sanic import Sanic
from uvloop.loop import Loop
from . import app


# noinspection PyUnusedLocal
@app.listener('after_server_start')
async def start_informer(application: Sanic, loop: Loop):
    REST_LOGGER.info(f'REST server started on {application.host}:{application.port}\n')

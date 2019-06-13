from pkg.utils.logger import REST_LOGGER
from . import app


@app.listener('after_server_start')
async def start_informer(app, loop):
    REST_LOGGER.info(f'Server started at {app.host}:{app.port}')

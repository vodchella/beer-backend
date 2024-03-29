from pkg.constants.version import SERVER_VERSION_FULL
from pkg.rest import root as r
from pkg.constants.version import SOFTWARE_VERSION
from pkg.decorators import app_context
from sanic import response
from sanic.request import Request
from sanic_openapi import doc


#
#  Общие для всех версий
#


# noinspection PyUnusedLocal
@r.get('/')
@doc.summary('Возвращает наименование сервера и версию ПО')
@app_context
async def root(request: Request):
    return response.json({
        'software': SOFTWARE_VERSION,
    })


# noinspection PyUnusedLocal
@r.get('/ping')
@doc.summary('Возвращает версию ПО')
@app_context
async def ping(context):
    return response.json({'version': SERVER_VERSION_FULL})


#
#  Статика
#


r.static('/favicon.png', './pkg/rest/static/images/favicon.png')
r.static('/favicon.ico', './pkg/rest/static/images/favicon.ico')

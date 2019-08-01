from pkg.rest import app
from pkg.constants.version import SOFTWARE_VERSION
from pkg.decorators import app_context
from sanic import response
from sanic.request import Request


#
#  Главная страница
#


# noinspection PyUnusedLocal
@app.get('/')
@app_context
async def root(request: Request):
    return response.json({
        'software': SOFTWARE_VERSION,
    })


#
#  Статика
#


app.static('/favicon.png', './pkg/rest/static/images/favicon.png')
app.static('/favicon.ico', './pkg/rest/static/images/favicon.ico')

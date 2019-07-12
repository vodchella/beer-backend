from pkg.rest import app
from pkg.constants.version import SOFTWARE_VERSION
from pkg.decorators import rest_context
from sanic import response


#
#  Главная страница
#


# noinspection PyUnusedLocal
@app.get('/')
@rest_context
async def root(context):
    return response.json({
        'software': SOFTWARE_VERSION,
    })


#
#  Статика
#


app.static('/favicon.png', './pkg/rest/static/images/favicon.png')
app.static('/favicon.ico', './pkg/rest/static/images/favicon.ico')

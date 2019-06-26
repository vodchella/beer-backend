from pkg.app import app
from pkg.constants.version import SOFTWARE_VERSION
from pkg.decorators import rest_context
from sanic import response


#
#  Главная страница
#


@app.get('/')
@rest_context
async def ping(context):
    return response.json({
        'software': SOFTWARE_VERSION,
    })


#
#  Статика
#


app.static('/favicon.png', './pkg/app/static/images/favicon.png')
app.static('/favicon.ico', './pkg/app/static/images/favicon.ico')

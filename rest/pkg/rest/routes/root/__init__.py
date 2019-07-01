from pkg.rest import app
from pkg.constants.version import SOFTWARE_VERSION
from pkg.decorators import rest_context, authenticated
from sanic import response


#
#  Главная страница
#


@app.get('/')
@rest_context
async def root(context):
    return response.json({
        'software': SOFTWARE_VERSION,
    })


@app.get('/test_jwt')
@rest_context
@authenticated
async def root(context):
    return response.json({
        'result': 'ok',
    })


#
#  Статика
#


app.static('/favicon.png', './pkg/app/static/images/favicon.png')
app.static('/favicon.ico', './pkg/app/static/images/favicon.ico')

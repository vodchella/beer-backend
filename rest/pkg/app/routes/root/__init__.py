from pkg.app import app
from pkg.constants.version import SOFTWARE_VERSION
from pkg.decorators import handle_exceptions
from sanic import response


#
#  Главная страница
#


@app.get('/')
@handle_exceptions
async def ping(request):
    from pkg.models import User
    user = await app.db.aio.select(app.db.SelectQuery(User))

    return response.json({'software': SOFTWARE_VERSION, 'user': user})


#
#  Статика
#


app.static('/favicon.png', './pkg/app/static/images/favicon.png')
app.static('/favicon.ico', './pkg/app/static/images/favicon.ico')

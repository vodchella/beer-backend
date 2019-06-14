from pkg.app import app
from pkg.constants.version import SOFTWARE_VERSION
from pkg.decorators import handle_exceptions
from playhouse.shortcuts import model_to_dict
from sanic import response


#
#  Главная страница
#


@app.get('/')
@handle_exceptions
async def ping(request):
    from pkg.models import User
    result = await app.db.aio.select(app.db.SelectQuery(User))
    for user in result:
        pass

    return response.json({'software': SOFTWARE_VERSION, 'user': model_to_dict(user, exclude='aio')})


#
#  Статика
#


app.static('/favicon.png', './pkg/app/static/images/favicon.png')
app.static('/favicon.ico', './pkg/app/static/images/favicon.ico')

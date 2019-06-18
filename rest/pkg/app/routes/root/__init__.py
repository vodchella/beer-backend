from pkg.app import app
from pkg.constants.version import SOFTWARE_VERSION
from pkg.decorators import rest_context
from pkg.utils.peewee import fetch_one, model_to_json, generate_unique_id
from sanic import response


#
#  Главная страница
#


@app.get('/')
@rest_context
async def ping(context):
    from pkg.models import User
    result = await app.db.aio.select(User.select().where(User.user_id == 'DaNhiRv862lsVbGx'))
    user = fetch_one(result)

    return response.json({
        'software': SOFTWARE_VERSION,
        'some_id': generate_unique_id(),
        'user': model_to_json(user)
    })


#
#  Статика
#


app.static('/favicon.png', './pkg/app/static/images/favicon.png')
app.static('/favicon.ico', './pkg/app/static/images/favicon.ico')

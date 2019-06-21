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
    from pkg.models import User, Company, ServicePoint, Employee, Card

    result = await app.db.aio.select(User.select().where(User.user_id == 'DaNhiRv862lsVbGx'))
    user = fetch_one(result)

    result = await app.db.aio.select(Company.select().where(Company.is_active))
    company = fetch_one(result)

    result = await app.db.aio.select(ServicePoint.select().where(ServicePoint.company_id == 'hLL04DwaV9oGzF3n'))
    service_point = fetch_one(result)

    result = await app.db.aio.select(Employee.select())
    employee = fetch_one(result)

    result = await app.db.aio.select(Card.select().where(Card.attributes.contains('name')))
    card = fetch_one(result)
    card_dict = model_to_json(card)

    await app.db.aio.update(Card.update(
        attributes=Card.attributes.concat({'value': card_dict['attributes']['value'] + 1})
    ))

    return response.json({
        'software': SOFTWARE_VERSION,
        'some_id': generate_unique_id(),
        'company': model_to_json(company),
        'service_point': model_to_json(service_point),
        'employee': model_to_json(employee),
        'card': model_to_json(card),
        'user': model_to_json(user)
    })


#
#  Статика
#


app.static('/favicon.png', './pkg/app/static/images/favicon.png')
app.static('/favicon.ico', './pkg/app/static/images/favicon.ico')

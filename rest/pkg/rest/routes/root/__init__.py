import jwt
from pkg.rest import app
from pkg.constants.version import SOFTWARE_VERSION
from pkg.decorators import rest_context
from sanic import response


#
#  Главная страница
#
from pkg.services.user_service import UserService
from pkg.utils.errors import response_403
from pkg.utils.jwt import create_secret


@app.get('/')
@rest_context
async def root(context):
    return response.json({
        'software': SOFTWARE_VERSION,
    })


@app.get('/test_jwt')
@rest_context
async def root(context):
    headers = context.request.headers
    authorization = headers.get('authorization', None)
    if authorization:
        token = authorization[len('Bearer '):]
        payload = jwt.decode(token, verify=False)
        user = await UserService.find(payload.get('uid', None))
        if user:
            secret = create_secret(user)
            try:
                decoded = jwt.decode(token, secret, algorithms='HS256')
                return response.json({
                    'result': decoded,
                })
            except:
                return response_403(context.request)
        else:
            return response_403(context.request)
    else:
        return response_403(context.request)


#
#  Статика
#


app.static('/favicon.png', './pkg/app/static/images/favicon.png')
app.static('/favicon.ico', './pkg/app/static/images/favicon.ico')

from pkg.utils.console import panic
from pkg.utils.logger import LOG_CONFIG
from sanic import Sanic, Blueprint


try:
    app = Sanic(__name__, log_config=LOG_CONFIG)

    app.config.API_VERSION = '1.0.0'
    app.config.API_TITLE = 'MyBeer API'
    app.config.API_CONTACT_EMAIL = 'twister.kz@gmail.com'

    root = Blueprint('Root', url_prefix='/')
    cards = Blueprint('Cards', url_prefix='/api/v1/cards')
    users = Blueprint('Users', url_prefix='/api/v1/users')
except:
    panic()

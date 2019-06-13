from pkg.utils.console import panic
from pkg.utils.logger import LOG_CONFIG
from sanic import Sanic, Blueprint


try:
    app = Sanic(__name__, log_config=LOG_CONFIG)
    v1 = Blueprint('v1', url_prefix='/api/v1')
except:
    panic()


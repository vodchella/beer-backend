import os
import yaml
from pkg.utils.console import panic
from pkg.utils.files import read_file

try:
    CFG_FILE = (os.environ['BEER_REST_CONFIG'] if 'BEER_REST_CONFIG' in os.environ else None) or 'config.yml'
    CONFIG = yaml.load(read_file(CFG_FILE), Loader=yaml.BaseLoader)
except FileNotFoundError:
    panic()

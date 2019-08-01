from behave.runner import Context
from tests.behave.utils import checked_behave_request


# noinspection PyUnusedLocal
def before_all(context: Context):
    json = checked_behave_request('GET', 'http://localhost:8517/')
    if 'software' not in json:
        raise Exception('Invalid response format')
    if not json['software'].startswith('MyBeer REST server v'):
        raise Exception('Invalid software version')

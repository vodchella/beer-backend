from tests.behave.utils import checked_behave_request


def before_all(context):
    json = checked_behave_request('get', 'http://localhost:8517/')
    if 'software' not in json:
        raise Exception('Invalid response format')
    if not json['software'].startswith('MyBeer REST server v'):
        raise Exception('Invalid software version')

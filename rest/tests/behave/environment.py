from tests.behave.utils import checked_request


def before_all(context):
    response = checked_request('get', 'http://localhost:8517/')
    software = response.json()['software']
    if not software.startswith('MyBeer REST server v'):
        raise Exception('Invalid software version')

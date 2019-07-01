import json
from json import JSONDecodeError
from requests import HTTPError, Session, request
from tests.behave.constants import PASSWORD, TEST_USER_PATH


def get_response_json(response):
    try:
        return response.json()
    except JSONDecodeError as e:
        raise Exception(f'JSONDecodeError: {e}\nINVALID JSON: {response.text}')


def behave_request(method, url, token=None, **kwargs):
    session = Session()
    headers = {
        'User-Agent': f'BEHAVE ({session.headers["User-Agent"]})'
    }
    if token:
        headers.update({'authorization': f'Bearer {token}'})
    return request(method, url,
                   headers=headers,
                   **kwargs)


def authorized_behave_request(method, url, **kwargs):
    login_url = f'{TEST_USER_PATH}/login/password'
    payload = {'password': PASSWORD}
    tokens = json.loads(behave_request('GET', login_url, data=json.dumps(payload)).text)['result']
    return behave_request(method, url, token=tokens['auth'], **kwargs)


def checked_behave_request(method, url, **kwargs):
    response = behave_request(method, url, **kwargs)
    try:
        response.raise_for_status()
    except HTTPError as e:
        json = get_response_json(response)
        raise Exception(f'{e}\nRESPONSE: {json}')
    return get_response_json(response)

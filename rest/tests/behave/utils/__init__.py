import json
from json import JSONDecodeError
from requests import HTTPError, Session, request, Response
from tests.behave.utils.constants import PASSWORD, TEST_USER_PATH


def get_response_json(response: Response):
    try:
        return response.json()
    except JSONDecodeError as e:
        raise Exception(f'JSONDecodeError: {e}\nINVALID JSON: {response.text}')


def behave_request(method: str, url: str, token: str = None, **kwargs):
    session = Session()
    headers = {
        'User-Agent': f'BEHAVE ({session.headers["User-Agent"]})'
    }
    if token:
        headers.update({'authorization': f'Bearer {token}'})
    return request(method, url, headers=headers, **kwargs)


def authorized_behave_request(method: str, url: str, token_type: str = 'auth', **kwargs):
    login_url = f'{TEST_USER_PATH}/login'
    payload = {'password': PASSWORD}
    tokens = json.loads(behave_request('GET', login_url, params=payload).text)['result']
    return behave_request(method, url, token=tokens[token_type], **kwargs)


def checked_behave_request(method: str, url: str, **kwargs):
    response = behave_request(method, url, **kwargs)
    try:
        response.raise_for_status()
    except HTTPError as e:
        json_ = get_response_json(response)
        raise Exception(f'{e}\nRESPONSE: {json_}')
    return get_response_json(response)

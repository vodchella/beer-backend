from json import JSONDecodeError
from requests import HTTPError, Session, request


def get_response_json(response):
    try:
        return response.json()
    except JSONDecodeError as e:
        raise Exception(f'JSONDecodeError: {e}\nINVALID JSON: {response.text}')


def checked_request(method, url, **kwargs):
    session = Session()
    response = request(method,
                       url,
                       headers={
                           'User-Agent': f'BEHAVE ({session.headers["User-Agent"]})'
                       },
                       **kwargs)
    try:
        response.raise_for_status()
    except HTTPError as e:
        json = get_response_json(response)
        raise Exception(f'{e}\nRESPONSE: {json}')
    return get_response_json(response)

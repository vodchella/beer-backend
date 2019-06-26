from requests import HTTPError, request


def checked_request(method, url, **kwargs):
    response = request(method, url, **kwargs)
    try:
        response.raise_for_status()
    except HTTPError as e:
        json = response.json()
        raise Exception(f'{e}\nRESPONSE: {json}')
    return response

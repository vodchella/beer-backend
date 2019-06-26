import requests


def checked_request(method, url, **kwargs):
    response = requests.request(method, url, **kwargs)
    response.raise_for_status()
    return response

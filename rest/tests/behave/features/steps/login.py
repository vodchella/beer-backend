from behave import *
from behave.runner import Context
from tests.behave.utils.constants import *
from tests.behave.utils import behave_request


@given('I try to login with incorrect user ID')
def step_impl(context: Context):
    url = f'{USERS_PATH}/incorrectid/login'
    payload = '{"password": "' + PASSWORD + '"}'
    context.response = behave_request('GET', url, data=payload)


@given('I try to login with incorrect password')
def step_impl(context: Context):
    url = f'{TEST_USER_PATH}/login'
    payload = '{"password": "incorrect"}'
    context.response = behave_request('GET', url, data=payload)


@given('I send correct login data')
def step_impl(context: Context):
    url = f'{TEST_USER_PATH}/login'
    payload = '{"password": "' + PASSWORD + '"}'
    context.response = behave_request('GET', url, data=payload)


@then('I will get Ok http status and tokens')
def step_impl(context: Context):
    assert context.response.status_code == 200
    json_ = context.response.json()
    assert 'result' in json_
    result = json_['result']
    assert 'auth' in result and 'refresh' in result


@given('I try to login with invalid JSON')
def step_impl(context):
    url = f'{TEST_USER_PATH}/login'
    payload = 'invalid-json'
    context.response = behave_request('GET', url, data=payload)

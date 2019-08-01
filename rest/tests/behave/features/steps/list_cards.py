from behave import *
from behave.runner import Context
from tests.behave.utils.constants import USERS_PATH, TEST_USER_PATH
from tests.behave.utils import behave_request, authorized_behave_request


@given('I try to list cards with invalid bearer token')
def step_impl(context: Context):
    url = f'{TEST_USER_PATH}/cards'
    context.response = behave_request('GET', url)


@given('I try to list cards with invalid user ID')
def step_impl(context: Context):
    url = f'{USERS_PATH}/incorrectid/cards'
    context.response = authorized_behave_request('GET', url)


@given('I send correct data to list cards')
def step_impl(context: Context):
    url = f'{TEST_USER_PATH}/cards'
    context.response = authorized_behave_request('GET', url)


@then('I will get Ok http status and array of cards')
def step_impl(context: Context):
    assert context.response.status_code == 200
    json_ = context.response.json()
    assert 'result' in json_
    result = json_['result']
    assert isinstance(result, list)

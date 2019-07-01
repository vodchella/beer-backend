from behave import *
from tests.behave.constants import TEST_USER_PATH
from tests.behave.utils import behave_request


@given('I try to login with invalid JSON')
def step_impl(context):
    url = f'{TEST_USER_PATH}/login/password'
    payload = 'invalid-json'
    context.response = behave_request('GET', url, data=payload)

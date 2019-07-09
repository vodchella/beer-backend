from behave import *
from tests.behave.utils.constants import TEST_USER_PATH
from tests.behave.utils import authorized_behave_request


@given('I try to execute some request with "refresh" token')
def step_impl(context):
    url = f'{TEST_USER_PATH}/change-password'
    payload = '{"old": "11111", "new": "11111"}'
    context.response = authorized_behave_request('POST', url, token_type='refresh', data=payload)


@given('I try to execute "/refresh-tokens" with "auth" token')
def step_impl(context):
    url = f'{TEST_USER_PATH}/refresh-tokens'
    context.response = authorized_behave_request('GET', url)


@given('I try to execute "/refresh-tokens" with "refresh" token')
def step_impl(context):
    url = f'{TEST_USER_PATH}/refresh-tokens'
    context.response = authorized_behave_request('GET', url, token_type='refresh')

from behave import *
from tests.behave.constants import TEST_USER_PATH, USERS_PATH
from tests.behave.utils import authorized_behave_request


@given('I try to change password with invalid JSON')
def step_impl(context):
    url = f'{TEST_USER_PATH}/change-password'
    payload = 'invalid-json'
    context.response = authorized_behave_request('POST', url, data=payload)


@given('I try to change password with incorrect user ID')
def step_impl(context):
    url = f'{USERS_PATH}/incorrect-@@/change-password'
    context.response = authorized_behave_request('POST', url)


@given('I send incorrect data to change password')
def step_impl(context):
    url = f'{TEST_USER_PATH}/change-password'
    payload = '{"wrong_param": true}'
    context.response = authorized_behave_request('POST', url, data=payload)


@given('I send incorrect old password')
def step_impl(context):
    url = f'{TEST_USER_PATH}/change-password'
    payload = '{"old": "this is incorrect old password", "new": "some new password"}'
    context.response = authorized_behave_request('POST', url, data=payload)


@given('I send correct password data')
def step_impl(context):
    url = f'{TEST_USER_PATH}/change-password'
    # Не будем менять фактический пароль, дабы не сломать тесты
    # Хэш пароля в БД изменится
    payload = '{"old": "11111", "new": "11111"}'
    context.response = authorized_behave_request('POST', url, data=payload)

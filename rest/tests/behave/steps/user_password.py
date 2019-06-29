from behave import *
from tests.behave.utils import behave_request


USERS_PATH = 'http://localhost:8517/api/v1/users'
TEST_USER_PATH = f'{USERS_PATH}/DaNhiRv862lsVbGx'


@given('I send invalid JSON')
def step_impl(context):
    url = f'{TEST_USER_PATH}/change-password'
    payload = 'invalid-json'
    context.response = behave_request('POST', url, data=payload)


@given('I send incorrect user ID')
def step_impl(context):
    url = f'{USERS_PATH}/@@@-invalid-id-@@@'
    context.response = behave_request('POST', url)


@given('I send incorrect data to change password')
def step_impl(context):
    url = f'{TEST_USER_PATH}/change-password'
    payload = '{"wrong_param": true}'
    context.response = behave_request('POST', url, data=payload)


@given('I send incorrect old password')
def step_impl(context):
    url = f'{TEST_USER_PATH}/change-password'
    payload = '{"old": "this is incorrect old password", "new": "some new password"}'
    context.response = behave_request('POST', url, data=payload)


@given('I send correct password data')
def step_impl(context):
    url = f'{TEST_USER_PATH}/change-password'
    # Не будем менять фактический пароль, дабы не сломать тесты
    # Хэш пароля в БД изменится
    payload = '{"old": "11111", "new": "11111"}'
    context.response = behave_request('POST', url, data=payload)


@then('I will get "{http_error_code}" http error')
def step_impl(context, http_error_code):
    assert context.response.status_code == int(http_error_code)


@then('I will get "{http_error_code}" http error and "{app_error_code}" application error')
def step_impl(context, http_error_code, app_error_code):
    json = context.response.json()
    assert json['error']['code'] == int(app_error_code)
    assert context.response.status_code == int(http_error_code)


@then('I will get Ok http status and "{result}" result')
def step_impl(context, result):
    json = context.response.json()
    assert json['result'] == result
    assert context.response.status_code == 200

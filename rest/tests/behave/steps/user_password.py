from behave import *
from tests.behave.utils import behave_request


TEST_USER_PATH = 'http://localhost:8517/api/v1/users/DaNhiRv862lsVbGx'


@given('I send incorrect data to change password')
def step_impl(context):
    url = f'{TEST_USER_PATH}/change-password'
    payload = '{"wrong_param": true}'
    context.response = behave_request('POST', url, data=payload)


@then('I will get "{http_error_code}" http-error code')
def step_impl(context, http_error_code):
    assert context.response.status_code == int(http_error_code)

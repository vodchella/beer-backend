from behave import *


@then('I will get "{http_error_code}" http error')
def step_impl(context, http_error_code):
    assert context.response.status_code == int(http_error_code)


@then('I will get "{http_error_code}" http error with "{app_error_code}" application error')
def step_impl(context, http_error_code, app_error_code):
    json = context.response.json()
    assert json['error']['code'] == int(app_error_code)
    assert context.response.status_code == int(http_error_code)


@then('I will get "{http_error_code}" http error or "{http_error_code2}" http error with "{app_error_code}" app error')
def step_impl(context, http_error_code, http_error_code2, app_error_code):
    json = context.response.json()
    assert (context.response.status_code == int(http_error_code)) or \
        (context.response.status_code == int(http_error_code2) and json['error']['code'] == int(app_error_code))


@then('I will get Ok http status and "{result}" result')
def step_impl(context, result):
    json = context.response.json()
    assert json['result'] == result
    assert context.response.status_code == 200

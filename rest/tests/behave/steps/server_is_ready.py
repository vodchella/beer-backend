from behave import *
from tests.behave.utils import checked_request


@given('I send GET-request to http://localhost:8517/')
def step_impl(context):
    context.response = checked_request('get', 'http://localhost:8517/')


@then('I will see full software version')
def step_impl(context):
    json = context.response.json()
    software = json['software']
    assert software.startswith('MyBeer REST server v')

from behave import *
from tests.behave.utils.constants import CARDS_PATH
from tests.behave.utils import behave_request, authorized_behave_request


@given('I try to create card with invalid bearer token')
def step_impl(context):
    url = f'{CARDS_PATH}/create'
    context.response = behave_request('POST', url)


@given('I try to create card with invalid JSON body')
def step_impl(context):
    url = f'{CARDS_PATH}/create'
    payload = 'invalid-json'
    context.response = authorized_behave_request('POST', url, data=payload)


@given('I try to create card with invalid owner ID')
def step_impl(context):
    url = f'{CARDS_PATH}/create'
    payload = '{"owner_id": "invalid"}'
    context.response = authorized_behave_request('POST', url, data=payload)


@given('I try to create card with empty name')
def step_impl(context):
    url = f'{CARDS_PATH}/create'
    payload = '{"owner_id": "invalid", "name": " "}'
    context.response = authorized_behave_request('POST', url, data=payload)


@given('I send correct card data')
def step_impl(context):
    url = f'{CARDS_PATH}/create'
    payload = '{"owner_id": "DaNhiRv862lsVbGx", "name": "Test card"}'
    context.response = authorized_behave_request('POST', url, data=payload)


@then('I will get Ok http status and new card in result')
def step_impl(context):
    assert context.response.status_code == 200
    json_ = context.response.json()
    assert 'result' in json_
    result = json_['result']
    assert 'card_id' in result and 'card_number' in result

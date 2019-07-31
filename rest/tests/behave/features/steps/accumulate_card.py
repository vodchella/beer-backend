from behave import *
from tests.behave.utils.constants import CARDS_PATH
from tests.behave.utils import behave_request, authorized_behave_request


def create_new_card(card_type='accumulation'):
    url = f'{CARDS_PATH}/create'
    payload = '{"owner_id": "DaNhiRv862lsVbGx", "name": "Test ' + card_type + ' card", "type": "' + card_type + '"}'
    response = authorized_behave_request('POST', url, data=payload)
    return response.json()['result']


@given('I try to accumulate card with invalid bearer token')
def step_impl(context):
    url = f'{CARDS_PATH}/HY3jBpIsGIWJ6fdj/accumulate'
    context.response = behave_request('POST', url)


@given('I try to accumulate card with invalid card ID')
def step_impl(context):
    url = f'{CARDS_PATH}/invalid-id/accumulate'
    context.response = authorized_behave_request('POST', url)


@given('I try to accumulate card with invalid JSON body')
def step_impl(context):
    url = f'{CARDS_PATH}/HY3jBpIsGIWJ6fdj/accumulate'
    payload = 'invalid-json'
    context.response = authorized_behave_request('POST', url, data=payload)


@given('I send correct data to accumulate card')
def step_impl(context):
    new_card_id = create_new_card()['card_id']
    url = f'{CARDS_PATH}/{new_card_id}/accumulate'
    payload = '{"increase_by": 2}'
    context.response = authorized_behave_request('POST', url, data=payload)


@then('I will get Ok http status and modified card value')
def step_impl(context):
    assert context.response.status_code == 200
    json_ = context.response.json()
    assert 'result' in json_
    result = json_['result']
    assert 'attributes' in result
    attributes = result['attributes']
    assert 'value' in attributes
    value = attributes['value']
    assert value == 2
    assert 'is_active' in result
    is_active = result['is_active']
    assert is_active is True


@given('I send data to fulfill card')
def step_impl(context):
    new_card = create_new_card()
    new_card_id = new_card['card_id']
    limit = new_card['attributes']['limit']
    url = f'{CARDS_PATH}/{new_card_id}/accumulate'
    payload = '{"increase_by": ' + str(limit) + '}'
    context.response = authorized_behave_request('POST', url, data=payload)


@then('I will get Ok http status and disabled card')
def step_impl(context):
    assert context.response.status_code == 200
    json_ = context.response.json()
    assert 'result' in json_
    result = json_['result']
    assert 'is_active' in result
    is_active = result['is_active']
    assert is_active is False


@given('I try to accumulate disabled card')
def step_impl(context):
    new_card = create_new_card()
    new_card_id = new_card['card_id']
    limit = new_card['attributes']['limit']
    url = f'{CARDS_PATH}/{new_card_id}/accumulate'
    payload = '{"increase_by": ' + str(limit) + '}'
    authorized_behave_request('POST', url, data=payload)
    context.response = authorized_behave_request('POST', url, data=payload)


@given('I try to accumulate over limit')
def step_impl(context):
    new_card = create_new_card()
    new_card_id = new_card['card_id']
    limit = new_card['attributes']['limit']
    url = f'{CARDS_PATH}/{new_card_id}/accumulate'
    payload = '{"increase_by": ' + str(limit + 1) + '}'
    context.response = authorized_behave_request('POST', url, data=payload)


@given('I try to accumulate nonaccumulatable card')
def step_impl(context):
    new_card_id = create_new_card(card_type='discount')['card_id']
    url = f'{CARDS_PATH}/{new_card_id}/accumulate'
    payload = '{"increase_by": 2}'
    context.response = authorized_behave_request('POST', url, data=payload)

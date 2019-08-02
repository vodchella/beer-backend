from behave import *
from behave.runner import Context
from tests.behave.utils.constants import CARDS_PATH
from tests.behave.utils import behave_request, authorized_behave_request


@given('I try to view card with invalid bearer token')
def step_impl(context: Context):
    url = f'{CARDS_PATH}/HY3jBpIsGIWJ6fdj'
    context.response = behave_request('GET', url)


@given('I try to view card with invalid card ID')
def step_impl(context: Context):
    url = f'{CARDS_PATH}/invalid-id'
    context.response = authorized_behave_request('GET', url)


@given('I send correct data to view card')
def step_impl(context: Context):
    url = f'{CARDS_PATH}/HY3jBpIsGIWJ6fdj'
    context.response = authorized_behave_request('GET', url)


@then('I will get Ok http status and valid card in result')
def step_impl(context: Context):
    assert context.response.status_code == 200
    json_ = context.response.json()
    assert 'result' in json_
    result = json_['result']
    assert 'card_id' in result
    assert 'type_of_card' in result
    assert 'is_active' in result


@given('I try to view card which not belong to me')
def step_impl(context):
    url = f'{CARDS_PATH}/fsvV0P2q2dZ4nuL1'
    context.response = authorized_behave_request('GET', url)

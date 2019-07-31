from behave import *
from tests.behave.utils.constants import CARDS_PATH
from tests.behave.utils import behave_request, authorized_behave_request


@given("I try to accumulate card with invalid bearer token")
def step_impl(context):
    url = f'{CARDS_PATH}/HY3jBpIsGIWJ6fdj/accumulate'
    context.response = behave_request('POST', url)


@given("I try to accumulate card with invalid card ID")
def step_impl(context):
    url = f'{CARDS_PATH}/invalid-id/accumulate'
    context.response = authorized_behave_request('POST', url)

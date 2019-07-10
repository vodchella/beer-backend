from pkg.rest import v1
from pkg.constants.error_codes import ERROR_JSON_PARSING_EXCEPTION, ERROR_UNALLOWED_CARD_TYPE
from pkg.decorators import employee_rest_context
from pkg.services.card_service import CardService
from pkg.services.user_service import UserService
from pkg.utils.errors import response_400, response_404, response_error
from pkg.utils.peewee import model_to_json
from sanic import response


CARD_PATH = '/cards/<card_id:[A-z0-9]+>'


@v1.post(f'/cards/create')
@employee_rest_context
async def create_card(context):
    body = context.request.parsed_json
    if body:
        owner = await UserService.find(body.get('owner_id', None))
        name = body.get('name', None)
        if owner and name and len(name.strip()):
            card = await CardService.create(context.employee, owner, name)
            return response.json({'result': model_to_json(card)})
        else:
            return response_400(context.request)
    else:
        return response_error(ERROR_JSON_PARSING_EXCEPTION)


@v1.post(f'{CARD_PATH}/accumulate')
@employee_rest_context
async def accumulate_value(context, card_id):
    card = await CardService.find(card_id)
    if card:
        if card.type_of_card == 'accumulation':
            body = context.request.parsed_json
            if body:
                increase_by = body.get('increase_by', None)
                if increase_by and increase_by > 0:
                    card.attributes['value'] += increase_by
                    await CardService.update(card)
                    return response.json({'result': model_to_json(card)})
                else:
                    return response_400(context.request)
            else:
                return response_error(ERROR_JSON_PARSING_EXCEPTION)
        else:
            return response_error(ERROR_UNALLOWED_CARD_TYPE)
    else:
        return response_404(context.request)

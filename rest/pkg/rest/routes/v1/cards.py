from pkg.rest import cards
from pkg.constants.error_codes import *
from pkg.constants.regexp import REGEXP_ID
from pkg.decorators import employee_app_context, json_request, authenticated_app_context
from pkg.models.card_attributes import CARD_ATTRIBUTE_CLASSES, AccumulationCardAttributes
from pkg.services.card_service import CardService
from pkg.services.user_service import UserService
from pkg.utils.context import get_current_context
from pkg.utils.dicts import copy_dict_and_exclude_keys
from pkg.utils.errors import response_error
from pkg.utils.peewee import model_to_json_object
from pkg.utils.responses import response_400, response_404, response_403, response_ok, response_403_short
from sanic.request import Request
from sanic_openapi import doc

CARD_PATH = f'/<card_id:{REGEXP_ID}>'


# noinspection PyUnusedLocal
@cards.post(f'/create')
@doc.summary('Создаёт новую карту')
@employee_app_context
@json_request
async def create_card(request: Request):
    ctx = get_current_context()
    owner = await UserService.find(ctx.json_body.get('owner_id', None))
    if owner:
        card_type = ctx.json_body.get('type', None)
        if card_type and card_type in CARD_ATTRIBUTE_CLASSES.keys():
            attrs = copy_dict_and_exclude_keys(ctx.json_body, 'owner_id', 'type')
            card = await CardService.create(owner, card_type, attrs)
            return response_ok(model_to_json_object(card))
        else:
            return response_error(ERROR_UNALLOWED_CARD_TYPE)
    return response_400()


# noinspection PyUnusedLocal
@cards.get(f'{CARD_PATH}')
@doc.summary('Возвращает карту по ID')
@authenticated_app_context
async def view_card(request: Request, card_id: str):
    card = await CardService.find(card_id)
    if card:
        ctx = get_current_context()
        if card.owner_id == ctx.user.user_id:
            return response_ok(model_to_json_object(card))
        else:
            return response_403_short()
    return response_404()


# noinspection PyUnusedLocal
@cards.post(f'{CARD_PATH}/accumulate')
@doc.summary('Увеличивает счётчик на накопительной карте')
@employee_app_context
@json_request
async def accumulate_value(request: Request, card_id: str):
    card = await CardService.find(card_id)
    if card:
        if card.type_of_card == 'accumulation':
            if card.is_active:
                ctx = get_current_context()
                if ctx.employee.company_id == card.company_id:
                    increase_by = ctx.json_body.get('increase_by', None)
                    if increase_by and increase_by > 0:
                        attributes = AccumulationCardAttributes(card.attributes)

                        new_value = attributes.value + increase_by
                        if attributes.limit > 0:
                            if new_value > attributes.limit:
                                return response_error(ERROR_CARD_LIMIT_EXCEEDED)
                            elif new_value == attributes.limit:
                                card.is_active = False
                        attributes.value = new_value

                        card.attributes = attributes.get_dict()
                        await CardService.update(card)

                        msg = 'Card was deactivated because of fullfilled' if not card.is_active else None
                        return response_ok(model_to_json_object(card), message=msg)
                    else:
                        return response_400()
                else:
                    return response_403()
            else:
                return response_error(ERROR_CARD_IS_NOT_ACTIVE)
        else:
            return response_error(ERROR_UNALLOWED_CARD_TYPE)
    else:
        return response_404()

from pkg.rest import v1
from pkg.constants.error_codes import *
from pkg.decorators import employee_app_context, json_request, authenticated_app_context
from pkg.services.card_service import CardService
from pkg.services.user_service import UserService
from pkg.utils.context import get_current_context
from pkg.utils.errors import response_error
from pkg.utils.peewee import model_to_json_object
from pkg.utils.responses import response_400, response_404, response_403, response_ok, response_403_short
from sanic.request import Request

CARD_PATH = '/cards/<card_id:[A-z0-9]+>'


# noinspection PyUnusedLocal
@v1.post(f'/cards/create')
@employee_app_context
@json_request
async def create_card(request: Request):
    ctx = get_current_context()
    owner = await UserService.find(ctx.json_body.get('owner_id', None))
    if owner:
        card_type = ctx.json_body.get('type', None)
        if card_type and card_type in ['accumulation', 'discount']:
            name = ctx.json_body.get('name', None)
            attr = {'name': name} if name and len(name.strip()) else {}
            card = await CardService.create(owner, card_type, attr)
            return response_ok(model_to_json_object(card))
        else:
            return response_error(ERROR_UNALLOWED_CARD_TYPE)
    return response_400()


@v1.get(f'{CARD_PATH}')
@authenticated_app_context
async def view_card(request: Request, card_id: str):
    card = await CardService.find(card_id)
    if card:
        ctx = get_current_context()
        if card.owner_id == ctx.user.user_id:
            return response_ok(model_to_json_object(card))
        else:
            return response_403_short()
    return response_404(request)


@v1.post(f'{CARD_PATH}/accumulate')
@employee_app_context
@json_request
async def accumulate_value(request: Request, card_id: str):
    card = await CardService.find(card_id)
    if card:
        if card.type_of_card == 'accumulation':
            if card.is_active:
                ctx = get_current_context()
                if ctx.employee.company_id == card.company_id:  # TODO: make test for this compare
                    increase_by = ctx.json_body.get('increase_by', None)
                    if increase_by and increase_by > 0:
                        new_value = card.attributes['value'] + increase_by

                        limit = card.attributes.get('limit', 0)
                        if limit > 0:
                            if new_value > limit:
                                return response_error(ERROR_CARD_LIMIT_EXCEEDED)
                            elif new_value == limit:
                                card.is_active = False

                        card.attributes['value'] = new_value
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
        return response_404(request)

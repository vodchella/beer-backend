from pkg.rest import v1
from pkg.constants.error_codes import ERROR_JSON_PARSING_EXCEPTION
from pkg.decorators import authenticated_rest_context
from pkg.services.card_service import CardService
from pkg.services.employee_service import EmployeeService
from pkg.services.user_service import UserService
from pkg.utils.errors import response_400, response_403_short, response_error
from pkg.utils.peewee import model_to_json
from sanic import response


@v1.post(f'/cards/create')
@authenticated_rest_context
async def create_card(context):
    employee = await EmployeeService.find_by_user_id(context.user.user_id)
    if employee and employee.is_active:
        body = context.request.parsed_json
        if body:
            owner = await UserService.find(body.get('owner_id', None))
            if owner:
                card = await CardService.create(employee, owner)
                return response.json({'result': model_to_json(card)})
            else:
                return response_400(context.request)
        else:
            return response_error(ERROR_JSON_PARSING_EXCEPTION, 'Invalid JSON')
    return response_403_short()

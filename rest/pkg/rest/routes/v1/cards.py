from pkg.rest import v1
from pkg.decorators import authenticated_rest_context
from pkg.services.employee_service import EmployeeService
from pkg.utils.errors import response_403
from pkg.utils.peewee import model_to_json
from sanic import response


@v1.post(f'/cards/create')
@authenticated_rest_context
async def create_card(context):
    current_user = context.user
    employee = await EmployeeService.find_by_user_id(current_user.user_id)
    if employee and employee.is_active:
        return response.json({'result': model_to_json(employee)})
    return response_403(context.request, log_stacktrace=False, log_error=False)

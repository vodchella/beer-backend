from pkg.models import Employee
from pkg.utils.context import get_current_context


class EmployeeService:
    @staticmethod
    async def find_by_user_id(user_id: str):
        ctx = get_current_context()
        try:
            return await ctx.db.get(Employee, Employee.user_id == user_id)
        except:
            return None

from pkg.models import Employee
from pkg.rest import app


class EmployeeService:
    @staticmethod
    async def find_by_user_id(user_id):
        try:
            return await app.db.aio.get(Employee, Employee.user_id == user_id)
        except:
            return None

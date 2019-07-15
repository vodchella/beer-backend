from pkg.models import Company
from pkg.services.service_point_service import ServicePointService
from pkg.utils.context import get_current_context


class CompanyService:
    @staticmethod
    async def find_by_service_point_id(service_point_id):
        ctx = get_current_context()
        try:
            service_point = await ServicePointService.find(service_point_id)
            return await ctx.db.get(Company, Company.company_id == service_point.company_id)
        except:
            return None

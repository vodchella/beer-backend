from pkg.models import Company
from pkg.rest import app
from pkg.services.service_point_service import ServicePointService


class CompanyService:
    @staticmethod
    async def find_by_service_point_id(service_point_id):
        try:
            service_point = await ServicePointService.find(service_point_id)
            return await app.db.aio.get(Company, Company.company_id == service_point.company_id)
        except:
            return None

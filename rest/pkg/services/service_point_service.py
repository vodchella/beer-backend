from pkg.models import ServicePoint
from pkg.rest import app


class ServicePointService:
    @staticmethod
    async def find(service_point_id):
        try:
            return await app.db.aio.get(ServicePoint, ServicePoint.service_point_id == service_point_id)
        except:
            return None

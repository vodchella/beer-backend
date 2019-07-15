from pkg.models import ServicePoint
from pkg.utils.context import get_current_context


class ServicePointService:
    @staticmethod
    async def find(service_point_id):
        ctx = get_current_context()
        try:
            return await ctx.db.get(ServicePoint, ServicePoint.service_point_id == service_point_id)
        except:
            return None

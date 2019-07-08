from nanoid import generate
from pkg.constants.database import CARD_NUMBER_ALPHABET
from pkg.models import Card, Employee, User
from pkg.services.company_service import CompanyService
from pkg.utils.peewee import generate_unique_id


class CardService:
    @staticmethod
    def generate_number():
        return generate(CARD_NUMBER_ALPHABET, 8)

    @staticmethod
    async def create(issuer: Employee, owner: User):
        company = await CompanyService.find_by_service_point_id(issuer.service_point_id)
        return await Card.aio.create(card_id=generate_unique_id(),
                                     card_number=CardService.generate_number(),
                                     type_of_card='accumulation',
                                     company_id=company.company_id,
                                     owner_id=owner.user_id,
                                     issuer_id=issuer.employee_id,
                                     issued_in_service_point_id=issuer.service_point_id,
                                     )

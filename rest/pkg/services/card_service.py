from nanoid import generate
from pkg.constants.database import CARD_NUMBER_ALPHABET
from pkg.models import Card, User
from pkg.models.card_attributes import CARD_ATTRIBUTE_CLASSES
from pkg.services.company_service import CompanyService
from pkg.utils.context import get_current_context
from pkg.utils.peewee import generate_unique_id


class CardService:
    @staticmethod
    def generate_number():
        return generate(CARD_NUMBER_ALPHABET, 8)

    @staticmethod
    async def create(owner: User, card_type: str, attr: dict):
        card_attributes = CARD_ATTRIBUTE_CLASSES[card_type](optional_data=attr)
        ctx = get_current_context()
        issuer = ctx.employee
        company = await CompanyService.find_by_service_point_id(issuer.service_point_id)
        card_id = await ctx.db.insert(Card.insert(card_id=generate_unique_id(),
                                                  card_number=CardService.generate_number(),
                                                  type_of_card=card_type,
                                                  company_id=company.company_id,
                                                  owner_id=owner.user_id,
                                                  issuer_id=issuer.employee_id,
                                                  issued_in_service_point_id=issuer.service_point_id,
                                                  attributes=card_attributes.get_dict()))
        return await CardService.find(card_id)

    @staticmethod
    async def find(card_id: str):
        if card_id:
            ctx = get_current_context()
            try:
                return await ctx.db.get(Card, Card.card_id == card_id)
            except:
                return None

    @staticmethod
    async def find_by_user(user_id: str):
        if user_id:
            ctx = get_current_context()
            try:
                sql = Card.select() \
                          .where(Card.owner_id == user_id) \
                          .order_by(Card.created_at.desc())
                return await ctx.db.execute(sql)
            except:
                return None

    @staticmethod
    async def update(card: Card):
        ctx = get_current_context()
        await ctx.db.update(card)

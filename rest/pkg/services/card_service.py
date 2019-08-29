from nanoid import generate
from pkg.constants.database import CARD_NUMBER_ALPHABET
from pkg.models import Card, User
from pkg.services.company_service import CompanyService
from pkg.utils import StrictDict
from pkg.utils.context import get_current_context
from pkg.utils.peewee import generate_unique_id


class AccumulationCardAttributes(StrictDict):
    def __init__(self, init_dict):
        super().__init__(['limit', 'value', 'name'], init_dict)


def create_default_card_attributes(card_type, additional_data):
    def_attr = {'limit': 19, 'value': 0} if card_type == 'accumulation' else {}
    if additional_data:
        def_attr = {**def_attr, **additional_data}
    return def_attr


class CardService:
    @staticmethod
    def generate_number():
        return generate(CARD_NUMBER_ALPHABET, 8)

    @staticmethod
    async def create(owner: User, card_type: str, attr: dict):
        def_attr = create_default_card_attributes(card_type, attr)
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
                                                  attributes=def_attr))
        return await CardService.find(card_id)

    @staticmethod
    async def find(card_id: str):
        cls = AccumulationCardAttributes({'limit': 19, 'value': 1})
        print(cls.value)
        print(cls['limit'])
        print(cls)

        ctx = get_current_context()
        try:
            return await ctx.db.get(Card, Card.card_id == card_id)
        except:
            return None

    @staticmethod
    async def find_by_user(user_id: str):
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

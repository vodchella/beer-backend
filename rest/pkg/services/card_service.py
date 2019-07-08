from pkg.models import Card


class CardService:
    @staticmethod
    async def create():
        return await Card.aio.create(card_id='test-identifier')

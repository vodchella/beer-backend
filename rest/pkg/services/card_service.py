from nanoid import generate
from pkg.constants.database import CARD_NUMBER_LENGTH, CARD_NUMBER_ALPHABET
from pkg.models import Card
from pkg.utils.peewee import generate_unique_id


class CardService:
    @staticmethod
    def generate_number():
        return generate(CARD_NUMBER_ALPHABET, CARD_NUMBER_LENGTH)

    @staticmethod
    async def create():
        return await Card.aio.create(card_id=generate_unique_id(),
                                     card_number=CardService.generate_number(),
                                     )

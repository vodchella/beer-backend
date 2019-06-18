from nanoid import generate
from pkg.constants.database import ID_FIELD_ALPHABET, ID_FIELD_LENGTH
from playhouse.shortcuts import model_to_dict


def fetch_one(async_result):
    result = list(async_result)
    return result[0] if len(result) else None


def model_to_json(model):
    if model:
        return model_to_dict(model, exclude='aio')


def generate_unique_id():
    # ~4 million years needed (speed: 1000 IDs per hour),
    # in order to have a 1% probability of at least one collision with current params
    # https://zelark.github.io/nano-id-cc/
    return generate(ID_FIELD_ALPHABET, ID_FIELD_LENGTH)

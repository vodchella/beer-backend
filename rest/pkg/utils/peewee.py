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
    return generate(ID_FIELD_ALPHABET, ID_FIELD_LENGTH)

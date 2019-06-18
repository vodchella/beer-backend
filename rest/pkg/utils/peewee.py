from playhouse.shortcuts import model_to_dict


def fetch_one(async_result):
    result = list(async_result)
    return result[0] if len(result) else None


def model_to_json(model):
    if model:
        return model_to_dict(model, exclude='aio')

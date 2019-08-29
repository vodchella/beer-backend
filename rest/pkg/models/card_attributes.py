from pkg.utils.dicts import StrictDict


class CardAttributes(StrictDict):
    def __init__(self, allowed_attributes, required_data: dict, optional_data: dict):
        init_data = required_data
        if optional_data:
            init_data = {**init_data, **optional_data}
        super().__init__(allowed_attributes, init_data)


class AccumulationCardAttributes(CardAttributes):
    def __init__(self, required_data: dict = None, optional_data: dict = None):
        req_data = required_data or {'limit': 19, 'value': 0}
        super().__init__(['limit', 'value', 'name'], req_data, optional_data)


class DiscountCardAttributes(CardAttributes):
    def __init__(self, required_data: dict = None, optional_data: dict = None):
        super().__init__([], required_data, optional_data)


CARD_ATTRIBUTE_CLASSES = {
    'accumulation': AccumulationCardAttributes,
    'discount': DiscountCardAttributes,
}

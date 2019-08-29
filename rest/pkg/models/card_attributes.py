from pkg.utils.dicts import StrictDict


class CardAttributes(StrictDict):
    def __init__(self, allowed_attributes, required_data: dict, optional_data: dict):
        init_data = required_data
        if optional_data:
            init_data = {**init_data, **optional_data}
        super().__init__(allowed_attributes, init_data)


class AccumulationCardAttributes(CardAttributes):
    def __init__(self, optional_data: dict):
        required_data = {'limit': 19, 'value': 0}
        super().__init__(['limit', 'value', 'name'], required_data, optional_data)


class DiscountCardAttributes(CardAttributes):
    def __init__(self, optional_data: dict):
        super().__init__([], {}, optional_data)


CARD_ATTRIBUTE_CLASSES = {
    'accumulation': AccumulationCardAttributes,
    'discount': DiscountCardAttributes,
}

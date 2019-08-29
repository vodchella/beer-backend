class StrictDict:
    _dict = {}
    _allowed_attributes = []

    def __init__(self, allowed_attributes, init_dict: dict):
        super().__init__()

        for key in init_dict.keys():
            if key not in allowed_attributes:
                raise Exception(f'Trying to set invalid attribute: {key}')

        self._allowed_attributes = allowed_attributes
        self._dict = init_dict

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getattr__(self, key):
        if key in self._allowed_attributes:
            return self._dict[key]
        else:
            raise Exception(f'Trying to get invalid attribute: {key}')

    def __setattr__(self, key, value):
        if key in ['_allowed_attributes', '_dict']:
            super().__setattr__(key, value)
        elif key in self._allowed_attributes:
            self._dict[key] = value
        else:
            raise Exception(f'Trying to set invalid attribute: {key}')

    def __str__(self):
        return str(self._dict)

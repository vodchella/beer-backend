import copy


def copy_dict_and_exclude_keys(input_dict: dict, *exclude_keys):
    result = copy.deepcopy(input_dict)
    for key in exclude_keys:
        result.pop(key, None)
    return result

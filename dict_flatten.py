def dict_flatten(target, separator, lkey=''):
    if not isinstance(target, dict):
        raise ValueError
    ret = OrderedDict()
    if not any(filter(lambda x: isinstance(x, (dict, list)), target.values())):
        return target

    ret = OrderedDict()
    for key, value in target.items():
        if isinstance(value, dict):
            for k, v in dict_flatten(value, separator).items():
                ret[key + separator + k] = v

        elif isinstance(value, list):
            for e in value:
                if isinstance(e, dict):
                    for k, v in dict_flatten(e, separator).items():
                        ret[key + separator + k] = v
                else:
                    ret[key] = e

        else:
            ret[key] = value
    return ret


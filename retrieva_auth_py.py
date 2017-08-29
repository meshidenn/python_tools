from typing import Dict

import datetime as dt
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib as hl


def add_api_signature(
    uri: str,
    data: str,
    api_key: str,
    secret_key: str,
    header: Dict[str, str] = {}
) -> (str, Dict[str, str]):

    if api_key is None and secret_key is None:
        return uri, header

    base_and_param = uri.split('?', 1)
    base = base_and_param[0]
    param = len(base_and_param) == 2 and base_and_param[1] or None
    current_time = format_date_time(mktime(dt.datetime.now().timetuple()))

    signature = data is not None and data.replace(' ', '').replace("\n", '') or ''
    parameters = param is not None and param.split('&') or []
    parameters.append("api_key={}".format(api_key))
    signature += ''.join(sorted(parameters))
    signature += current_time
    signature += secret_key

    encoded_signature = signature.encode('utf-8')
    parameters.append("api_signature={}".format(hl.md5(encoded_signature).hexdigest()))
    base += '?'
    base += '&'.join(parameters)
    ret_header = header.copy()
    ret_header.update({'Date': current_time})
    return base, ret_header

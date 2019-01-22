import json
from json import JSONDecodeError
from typing import Type

from storage import Storage


def get_err_msg(err: Exception) -> str:
    msg = ''
    if hasattr(err, 'message'):
        msg = err.message
    if hasattr(err, 'args') and len(err.args) > 0:
        msg = err.args[0]
    return msg


def to_int_if_possible(s: str):
    try:
        i = int(s)
    except (ValueError, TypeError):
        return s
    else:
        return i


def json_to_str(j) -> str:
    raw_json_str = json.loads(j)
    json_str = to_int_if_possible(raw_json_str)
    return json_str


def str_to_json(s: str):
    raw_json_obj = json.dumps(s)
    return raw_json_obj


def init_storage(storage_cls: Type[Storage], **kwargs):
    arguments = [arg[1][2:] for arg in storage_cls.get_arguments()]  # arg[1] is assumed to be of format --name
    try:
        feed = {arg.replace('-', '_'): kwargs[arg.replace('-', '_')] for arg in arguments}
    except KeyError:
        raise KeyError("The following variables missing: %s" % arguments)

    return storage_cls(**feed)

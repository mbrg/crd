from typing import Type
from os import environ

from storage import Storage


def init_storage(storage_cls: Type[Storage], *args, **kwargs):
    arguments = [arg[1][2:] for arg in storage_cls.get_arguments()]  # arg[1] is assumed to be of format --name
    try:
        feed = {arg.replace('-', '_'): environ[arg] for arg in arguments}
    except KeyError:
        raise KeyError("The following environment variables missing: %s" % arguments)

    return storage_cls(*args, **feed, **kwargs)


def get_descendents(cls, filtered_by: set = {}):
    """
    Given a Class cls, find and return a list of its descendents classes, which are not included in filtered_by
    """
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in get_descendents(c)]) - set(filtered_by)

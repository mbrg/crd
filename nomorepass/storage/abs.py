import collections
import abc
from typing import List, Tuple


class Storage(collections.MutableMapping):
    pass

    @classmethod
    @abc.abstractmethod
    def get_arguments(cls) -> List[Tuple[str, str, dict]]:
        pass

    def __str__(self):
        return '%s' % self.__class__.__name__

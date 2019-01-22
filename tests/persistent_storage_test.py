import pytest
from typing import Type
from os import environ

from crd.storage import Storage, VirtualStorage, init_storage
from tests.utils import get_descendents


@pytest.mark.parametrize("storage_cls", get_descendents(Storage, filtered_by={VirtualStorage}))
def test_open_close(storage_cls: Type[Storage]):

    strg = init_storage(storage_cls, **environ)
    strg['a'] = 1
    del strg

    strg = init_storage(storage_cls, **environ)
    assert strg.get('a') == 1

    # cleanup
    strg.clear()

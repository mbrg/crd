import pytest
from typing import Type

from storage import Storage, VirtualStorage
from tests.utils import get_descendents, init_storage


@pytest.mark.parametrize("storage_cls", get_descendents(Storage, filtered_by={VirtualStorage}))
def test_open_close(storage_cls: Type[Storage]):

    strg = init_storage(storage_cls)
    strg['a'] = 1
    del strg

    strg = init_storage(storage_cls)
    assert strg.get('a') == 1

    # cleanup
    strg.clear()

import pytest
from typing import Type
from os import environ

from storage import Storage, init_storage
from tests.utils import get_descendents


@pytest.mark.parametrize("storage_cls", get_descendents(Storage))
def test_key_error(storage_cls: Type[Storage]):

    strg = init_storage(storage_cls, **environ)

    with pytest.raises(KeyError):
        strg.pop("none existing key")

    with pytest.raises(KeyError):
        strg.popitem()

    with pytest.raises(KeyError):
        _ = strg["none existing key"]

    with pytest.raises(KeyError):
        del strg["none existing key"]

    # cleanup
    strg.clear()


@pytest.mark.parametrize("storage_cls", get_descendents(Storage))
def test_insertion_clear(storage_cls: Type[Storage]):

    strg = init_storage(storage_cls, **environ)
    strg['a'] = 1
    strg['a'] = 2
    strg['b'] = 3

    assert 2 == len(strg)
    assert 2 == len(strg.keys())
    assert 2 == len(strg.values())
    assert 2 == len(strg.items())

    strg.clear()
    assert 0 == len(strg)

    # cleanup
    strg.clear()


@pytest.mark.parametrize("storage_cls", get_descendents(Storage))
def test_copy(storage_cls: Type[Storage]):

    strg_1 = init_storage(storage_cls, **environ)
    strg_1['a'] = 1
    strg_1['a'] = 2
    strg_1['b'] = 3

    strg_2 = init_storage(storage_cls, **environ)
    strg_2.update(**strg_1)

    assert 2 == len(strg_2)
    assert 2 == len(strg_2.keys())
    assert 2 == len(strg_2.values())
    assert 2 == len(strg_2.items())

    del strg_2['a']
    assert 1 == len(strg_2)

    strg_2.clear()
    assert 0 == len(strg_2)

    # cleanup
    strg_1.clear()
    strg_2.clear()


@pytest.mark.parametrize("storage_cls", get_descendents(Storage))
def test_delete(storage_cls: Type[Storage]):

    strg = init_storage(storage_cls, **environ)
    strg['a'] = 1
    strg['a'] = 2
    strg['b'] = 3

    del strg['a']

    assert 1 == len(strg)

    # cleanup
    strg.clear()

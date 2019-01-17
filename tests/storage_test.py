import pytest

from storage import Storage


def get_descendents(cls):
    """
    Given a Class cls, find and return a list of its descendents classes
    """
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in get_descendents(c)])


@pytest.mark.parametrize("storage_cls", get_descendents(Storage))
def test_key_error(storage_cls):

    strg = storage_cls()

    with pytest.raises(KeyError):
        strg.pop("none existing key")

    with pytest.raises(KeyError):
        strg.popitem()

    with pytest.raises(KeyError):
        _ = strg["none existing key"]

    with pytest.raises(KeyError):
        del strg["none existing key"]


@pytest.mark.parametrize("storage_cls", get_descendents(Storage))
def test_insertion_deletion(storage_cls):

    strg_1 = storage_cls()

    strg_1['a'] = 1
    strg_1['a'] = 2
    strg_1['b'] = 3

    assert 2 == len(strg_1)
    assert 2 == len(strg_1.keys())
    assert 2 == len(strg_1.values())
    assert 2 == len(strg_1.items())

    ##

    strg_2 = strg_1.copy()

    assert 2 == len(strg_2)
    assert 2 == len(strg_2.keys())
    assert 2 == len(strg_2.values())
    assert 2 == len(strg_2.items())

    strg_2.clear()
    assert 0 == len(strg_2)
    assert 2 == len(strg_1)

    ##

    strg_3 = storage_cls(**strg_1)

    assert 2 == len(strg_3)
    assert 2 == len(strg_3.keys())
    assert 2 == len(strg_3.values())
    assert 2 == len(strg_3.items())

    strg_3.clear()
    assert 0 == len(strg_3)
    assert 2 == len(strg_1)

    ##

    strg_4 = strg_1.copy()
    del strg_4['a']

    assert 1 == len(strg_4)
    assert 2 == len(strg_1)

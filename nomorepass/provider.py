from model import Storage, StorageError


class VirtualStorage(Storage):
    """
    In-memory none-persistent Storage
    """

    def __init__(self):
        self._dict = {}

    def store(self, key: str, value: dict) -> None:
        if key in self._dict:
            raise StorageError
        else:
            self._dict[key] = value

    def update(self, key: str, value: dict) -> None:
        if key not in self._dict:
            raise StorageError
        else:
            self._dict[key] = value

    def delete(self, key: str) -> None:
        if key not in self._dict:
            raise StorageError
        else:
            del self._dict[key]

    def retrieve(self, key: str) -> dict:
        if key not in self._dict:
            raise StorageError
        else:
            return self._dict[key]

    def list(self) -> list:
        return list(self._dict.keys())

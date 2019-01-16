

class StorageError(Exception):
    pass


class Storage(object):
    """
    An abstract class which defines basic storage operations
    """

    def store(self, key: str, value: dict) -> None:
        """
        Store value under key
        """
        pass

    def update(self, key: str, value: dict) -> None:
        """
        Update value under key
        """
        pass

    def delete(self, key: str) -> None:
        """
        Delete (key, value) pair
        """
        pass

    def retrieve(self, key: str) -> dict:
        """
        Retrieve values under key
        """
        return {}

    def list(self) -> list:
        """
        List all available keys
        """
        return []


class CredentialStoreError(Exception):
    pass


class CredentialStore(object):
    """
    An abstract class which defines basic operations on a credentials storage
    """

    def __init__(self, storage: Storage):
        self._storage = storage

    def store_or_update(self, name: str, cred: dict) -> None:
        """
        Store creds under name key, or update if name already exists
        :param name: Secret unique name
        :param cred: Secret information as dict
        """
        try:
            self._storage.update(name, cred)
        except StorageError:
            self._storage.store(name, cred)

    def delete_if_exists(self, name: str) -> None:
        """
        Delete creds under name key, if such exists
        :param name: Secret unique name
        """
        try:
            self._storage.delete(name)
        except StorageError:
            pass

    def retrieve(self, name: str) -> dict:
        """
        Retrieve creds under name key, or empty dict if such are not found
        :param name: Secret unique name
        """
        return self._storage.retrieve(name)

    def list(self) -> list:
        """
        List credential names available in the CredentialStore
        """
        return self._storage.list()

    def retrieve_all(self, names: list = None) -> list:
        """
        Retrieve creds under each name in names. If names is None, all secrets are retrieved.
        :param names: Secret unique names
        :return: list of credentials, or Nones if a name is not found
        """
        if names is None:
            names = self.list()
        return [self.retrieve(name) for name in names]

    def store_or_update_all(self, names: list, creds: list) -> None:
        """
        store_or_update creds under each name in names
        :param names: secret unique names
        :param creds: list of dicts, which contain secret information
        """
        assert len(names) == len(creds), "names and creds lists should have the same length"

        for i in range(len(names)):
            self.store_or_update(names[i], creds[i])

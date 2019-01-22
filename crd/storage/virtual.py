import keyring
import json

from storage import Storage


class VirtualStorage(Storage):
    """
    In-memory none-persistent Storage
    """

    def __init__(self, *args, **kwargs):
        self._store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        self._store[key] = value

    def __delitem__(self, key):
        del self._store[key]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    @classmethod
    def get_arguments(cls):
        return []


class KeyringStorage(Storage):
    """
    Keyring-based persistent Storage
    """

    def __init__(self, service_name: str = "crd", keys_name: str = "$keys", *args, **kwargs):
        self._service = service_name

        # holds a list of current keys as a special secret
        self._keys = keys_name
        self._unmanaged_set(self._keys, [])

        self.update(dict(*args, **kwargs))

    @property
    def __key_set(self) -> set:
        return set(self[self._keys])

    def _unmanaged_set(self, key, value):
        try:
            secret = json.dumps(value)
            keyring.set_password(self._service, key, secret)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError('Secret for key %s must be Picklable' % key)

    def __getitem__(self, key):
        try:
            encoded_secret = keyring.get_password(self._service, key)
            secret = json.loads(encoded_secret)
        except (TypeError, json.JSONDecodeError) as e:
            if hasattr(e, 'message'):
                msg = e.message
            if hasattr(e, 'args') and len(e.args) > 0:
                msg = e.args[0]
            raise KeyError('TypeError: ' + msg)
        else:
            return secret

    def __setitem__(self, key, value):
        self._unmanaged_set(key, value)
        self._unmanaged_set(self._keys, list(self.__key_set.union({key})))

    def __delitem__(self, key):
        try:
            keyring.delete_password(self._service, key)
            self._unmanaged_set(self._keys, list(self.__key_set.difference({key})))
        except keyring.errors.PasswordDeleteError:
            raise KeyError

    def __iter__(self):
        return iter(self[self._keys])

    def __len__(self):
        return len(self[self._keys])

    @classmethod
    def get_arguments(cls):
        return [
            ("-s", "--service-name", dict(type=str, required=True, help="service name to use for keyring distinction")),
            ("-k", "--keys-name", dict(type=str, required=True, help="secret name to be used to keep track of keys saved to storage"))
        ]

import keyring

from crd.storage import Storage
from crd.storage.utils import get_err_msg, json_to_str, str_to_json, JSONDecodeError

import logging
logger = logging.getLogger("crd")


class VirtualStorage(Storage):
    """
    In-memory none-persistent Storage
    """

    def __init__(self, *args, **kwargs):
        self._store = dict()
        self.update(dict(*args, **kwargs))
        logger.info(str(self))

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

        self.update(dict(*args, **kwargs))
        logger.info("%s keys=%s" % (str(self), keys_name))

    @property
    def __key_set(self) -> set:
        keys_list = self[self._keys]
        return set([] if keys_list is None else keys_list)

    def _unmanaged_set(self, key: str, value):
        try:
            secret = str_to_json(value)
            keyring.set_password(self._service, key, secret)
        except JSONDecodeError as e:
            raise JSONDecodeError('Secret for key %s must be Pickle-able' % key, doc=e.doc, pos=e.pos)

    def __getitem__(self, key: str):
        try:
            encoded_secret = keyring.get_password(self._service, key)
            secret = json_to_str(encoded_secret)
        except (TypeError, JSONDecodeError) as e:
            raise KeyError('TypeError: ' + get_err_msg(e))
        else:
            return secret

    def __setitem__(self, key: str, value):
        self._unmanaged_set(key, value)
        self._unmanaged_set(self._keys, list(self.__key_set.union({key})))

    def __delitem__(self, key: str):
        try:
            keyring.delete_password(self._service, key)
            self._unmanaged_set(self._keys, list(self.__key_set.difference({key})))
        except keyring.errors.PasswordDeleteError:
            raise KeyError

    def __iter__(self):
        return iter(self[self._keys])

    def __len__(self):
        return len(self[self._keys])

    def __str__(self):
        return '%s(%s)' % (super(KeyringStorage, self).__str__(), self._service)

    @classmethod
    def get_arguments(cls):
        # noinspection PyPep8
        return [
            ("-s", "--service-name", dict(type=str, required=True, help="service name to use for keyring distinction")),
            ("-k", "--keys-name", dict(type=str, required=True, help="secret name to be used to keep track of keys saved to storage"))
        ]

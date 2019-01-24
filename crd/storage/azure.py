from azure.keyvault.models import KeyVaultErrorException
from azure.keyvault import KeyVaultClient, KeyVaultAuthentication, KeyVaultId
from msrest.exceptions import ClientRequestError

import adal

from datetime import datetime

from crd.storage import Storage
from crd.storage.virtual import KeyringStorage
from crd.storage.utils import to_int_if_possible

import logging
logger = logging.getLogger("crd")


class AzureKeyVaultStorage(Storage):
    """
    Azure KeyVault persistent Storage
    Based on: https://github.com/Azure/azure-sdk-for-python/blob/master/
              azure-keyvault/azure/keyvault/v2016_10_01/key_vault_client.py
              https://github.com/Azure-Samples/key-vault-python-authentication/
              blob/master/authentication_sample.py
    """

    # noinspection SpellCheckingInspection,SpellCheckingInspection
    CLIENT_ID = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'  # Azure CLI

    def _init_connection(self, tenant_id):

        auth_context = adal.AuthenticationContext('https://login.microsoftonline.com/%s' % tenant_id)

        def auth_handler(server, resource, scope):

            # retrieve last used token (if exists)
            token_key = str((server, resource, scope))
            token = self._mem.get(token_key, {'expiresOn': datetime.now()})

            # time to refresh token?
            if datetime.now() > datetime.strptime(token['expiresOn'], "%Y-%m-%d %H:%M:%S.%f"):
                user_code_info = auth_context.acquire_user_code(resource, self.CLIENT_ID)

                print(user_code_info['message'])
                token = auth_context.acquire_token_with_device_code(
                    resource=resource, client_id=self.CLIENT_ID, user_code_info=user_code_info)
                self._mem[token_key] = token

            return token['tokenType'], token['accessToken']

        conn = KeyVaultClient(KeyVaultAuthentication(auth_handler))

        # validate connection
        try:
            itr = conn.get_secrets(self._vault_uri, maxresults=1)
            next(itr)
        except ClientRequestError:
            raise ValueError("Connection error occurred. Please validate your arguments are correct: "
                             "vault=%s, tenant_id=%s" % (self._vault, tenant_id))
        except StopIteration:
            pass

        return conn

    def __init__(self, vault: str, tenant_id: str, *args, **kwargs):
        self._vault = vault

        self._mem = KeyringStorage(service_name='AzureKeyVaultStorage')  # persistent storage to hold session tokens
        self._conn = self._init_connection(tenant_id)

        self.update(dict(*args, **kwargs))
        logger.info("%s tenant=%s, vault=%s" % (str(self), tenant_id, vault))

    @property
    def _vault_uri(self):
        return "https://%s.vault.azure.net/" % self._vault

    def __getitem__(self, key):
        try:
            secret_bundle = self._conn.get_secret(self._vault_uri, key, KeyVaultId.version_none)
            secret_bundle_val = to_int_if_possible(secret_bundle.value)
            return secret_bundle_val
        except KeyVaultErrorException as e:
            raise KeyError('KeyVaultErrorException: ' + e.message)

    def __setitem__(self, key, value):
        self._conn.set_secret(self._vault_uri, key, value)

    def __delitem__(self, key):
        try:
            self._conn.delete_secret(self._vault_uri, key)
        except KeyVaultErrorException as e:
            raise KeyError('KeyVaultErrorException: ' + e.message)

    def __iter__(self):
        secret_item_paged = self._conn.get_secrets(self._vault_uri)

        for sec in secret_item_paged:
            yield sec.id.replace(self._vault_uri + 'secrets/', '')

    def __len__(self):
        return len(list(self.__iter__()))

    def __str__(self):
        return '%s(%s)' % (super(type(self), self).__str__(), self._vault)

    @classmethod
    def get_arguments(cls):
        return [
            ("-v", "--vault", dict(type=str, required=True, help="azure keyvault name")),
            ("-t", "--tenant-id", dict(type=str, required=True, help="azure-active-directory tenant id"))
        ]

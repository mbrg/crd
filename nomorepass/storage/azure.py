from azure.keyvault.models import KeyVaultErrorException, SecretItemPaged
from azure.keyvault import KeyVaultClient, KeyVaultAuthentication, KeyVaultId
import adal

from storage import Storage


class AzureKeyVaultStorage(Storage):
    """
    Azure KeyVault persistent Storage
    Based on: https://github.com/Azure/azure-sdk-for-python/blob/master/
              azure-keyvault/azure/keyvault/v2016_10_01/key_vault_client.py
              https://github.com/Azure-Samples/key-vault-python-authentication/
              blob/master/authentication_sample.py
    """

    @staticmethod
    def _init_connection(tenant_id, session_mem):

        auth_context = adal.AuthenticationContext('https://login.microsoftonline.com/%s' % tenant_id)
        xplat_client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46'  # Azure CLI

        def auth_handler(server, resource, scope):
            if (server, resource, scope) not in session_mem:
                user_code_info = auth_context.acquire_user_code(resource,
                                                                xplat_client_id)

                print(user_code_info['message'])
                session_mem[(server, resource, scope)] = auth_context.acquire_token_with_device_code(
                    resource=resource, client_id=xplat_client_id, user_code_info=user_code_info)

            token = session_mem[(server, resource, scope)]
            return token['tokenType'], token['accessToken']

        conn = KeyVaultClient(KeyVaultAuthentication(auth_handler))

        return conn

    def __init__(self, vault : str, tenant_id : str, *args, **kwargs):
        self._vault = vault

        self._session_mem = {}
        self._conn = self._init_connection(tenant_id, self._session_mem)

        self.update(dict(*args, **kwargs))

    @property
    def _vault_uri(self):
        return "https://%s.vault.azure.net/" % self._vault

    def __getitem__(self, key):
        try:
            secret_bundle = self._conn.get_secret(self._vault_uri, key, KeyVaultId.version_none)
            return secret_bundle.value
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
        return '%s(%s)' % (super(self, self.__class__).__str__(), self._vault)

    @classmethod
    def get_arguments(cls):
        return [
            ("-v", "--vault-name", dict(type=str, required=True, help="azure keyvault name")),
            ("-t", "--tenant-id", dict(type=str, required=True, help="azure-active-directory tenant id"))
        ]

from crd.storage.abs import Storage
#from crd.storage.azure import AzureKeyVaultStorage
from crd.storage.virtual import VirtualStorage, KeyringStorage
from crd.storage.utils import init_storage


# TODO:remove this
class AzureKeyVaultStorage(KeyringStorage):

    def __init__(self, *args, **kwargs):
        super(AzureKeyVaultStorage, self).__init__(*args, **kwargs)

    @classmethod
    def get_arguments(cls):
        return [
            ("-v", "--vault", dict(type=str, required=True, help="azure keyvault name")),
            ("-t", "--tenant-id", dict(type=str, required=True, help="azure-active-directory tenant id"))
        ]


MODELS = (
    ("virtual", "in-memory none-persistent storage", VirtualStorage),
    ("keyring", "Keyring-based persistent Storage", KeyringStorage),
    ("azure", "Azure KeyVault persistent storage", AzureKeyVaultStorage),
)

NAME_TO_MODEL = {m[0]: m[2] for m in MODELS}

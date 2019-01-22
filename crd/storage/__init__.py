from crd.storage.abs import Storage
from crd.storage.azure import AzureKeyVaultStorage
from crd.storage.virtual import VirtualStorage, KeyringStorage
from crd.storage.utils import init_storage

MODELS = (
    ("virtual", "in-memory none-persistent storage", VirtualStorage),
    ("keyring", "Keyring-based persistent Storage", KeyringStorage),
    ("azure", "Azure KeyVault persistent storage", AzureKeyVaultStorage),
)

NAME_TO_MODEL = {m[0]: m[2] for m in MODELS}

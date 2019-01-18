from .abs import Storage
from .azure import AzureKeyVaultStorage
from .virtual import VirtualStorage

models = (
    ("virtual", "in-memory none-persistent storage", VirtualStorage),
    ("azure", "Azure KeyVault persistent storage", AzureKeyVaultStorage),
)

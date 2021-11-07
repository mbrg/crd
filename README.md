Hi! I'm considering to revisit this project. If you're interested, please 👍 [crd 2.0](https://github.com/mbrg/crd/issues/3)
## *crd* - your private secret storage, with a familiar dict API

A simple secret manager which uses your own secret storage as backend.
_crd_ provides a familiar dict-like API access your secret storage, 
and a CLI to perform daily tasks (get/set/del secrets).

Install with: `pip install crd`

Quick reference:
 - [CLI usage samples](#cli-usage-samples)
   - [Configuration](#config)
   - [Usage](#usage)
 - [Storage API](#storage-api)
 - [Supported backends](#supported-backends)
   - [Azure](#azure)
   - [Secured locally](#secured-locally)
   - [Virtual](#virtual)


## CLI usage samples

### Config

```bash
# show current configuratiom
$ cfg config --show

# configure local persistent storage, secured by your platform credentials
$ cfg config keyring

# configure Azure-based persistent storage, secured by Azure KeyVault and Azure Active Directory
$ cfg config azure -v MY_KEYVAULT_NAME -t MY_TENANT_GUID
```

### Usage
```bash
# store a new secret
$ cfg set -k my_github_creds        
crd > Secret: ****
crd > Secret my-github-creds stored safely.

# retrieve a secret
$ cfg get -k git        
crd > Found 2 options:
        0 | my-git-creds
        1 | my-github-creds
crd > Choose {0..1} or q to quit: 1
crd > Secret my-github-creds was copied to clipboard.

# delete a secret
$crd del -k my-git-creds
crd > Are you sure you want to delete secret my-git-creds? (y/Y) to accept: y
crd > Secret my-git-creds deleted successfully.
```

## Storage API

_crd_ provides a familiar dict-like API for secret storage.

Here are a few usage examples:

``` python
from crd.storage import AzureKeyVaultStorage, KeyringStorage, VirtualStorage

# init Storage object, uncomment lines bellow to use other storage backends
strg = AzureKeyVaultStorage(vault=MY_KEYVAULT_NAME, tenant_id=MY_TENANT_GUID)
# strg = KeyringStorage()
# strg = VirtualStorage() 

# Use storage like you would use a Python dict
strg["my-github-pass"] = "MY_PASS"
strg["my-github-pass"] = "MY_NEW_PASS"
strg["my-git-pass"] = "MY_OTHER_PASS"

print(len(strg))
# 2

for key in strg:
    print(key):
# my-git-pass
# my-github-pass

del strg['my-git-pass']
print(len(strg))
# 1
```


## Supported backends

### Azure

`AzureKeyVaultStorage` - Azure-based persistent storage, secured by Azure KeyVault and Azure Active Directory

How to:

- [Create your own][1] Azure KeyVault and copy the vault name (_Contoso-Vault2_ for example)
- Copy your tenant id from 
[Azure portal -> Azure Active Directory -> Properties -> Directory ID][2]
(_e887307a-6b6b-4404-b00b-bcc673928db6_ for example)
- Configure _crd_ by running: `$ cfg config azure -v Contoso-Vault2 -t e887307a-6b6b-4404-b00b-bcc673928db6`


[1]: https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/Properties
[2]: https://docs.microsoft.com/en-us/azure/key-vault/quick-create-portal

### Secured locally

`KeyringStorage` - Platform-agnostic local persistent storage, secured by your platform credentials

How to:

- Configure `crd` by running: `$ cfg config keyring`

### Virtual

`VirtualStorage` - In-memory none-persistent storage, to be used for debugging only (not secure).

How to:

- Configure `crd` by running: `$ cfg config virtual`


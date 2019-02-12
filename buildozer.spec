[app]

# (str) Title of your application
title = Hush

# (str) Package name
package.name = hush

# (str) Package domain (needed for android/ios packaging)
package.domain = mibarg.hush

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

android.permissions = INTERNET

orientation = all

requirements = python3crystax,kivy,argparse,azure-keyvault,msrest,adal,keyring,pyperclip

android.ndk_path = /opt/crystax-ndk-10.3.2

[buildozer]
log_level = 2

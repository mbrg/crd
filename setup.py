from setuptools import setup, find_packages

setup(
    name='crd',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/mibarg/crd',
    license='MIT',
    author='mibarg',
    author_email='mibarg@users.noreply.github.com',
    description='Your private secret storage, with a familiar dict API',
    install_requires=[
        'azure-keyvault',
        'msrest',
        'adal',
        'argparse',
        'pyperclip',
        'getpass'
    ],
    scripts=['crd/main.py'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)

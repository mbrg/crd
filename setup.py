from setuptools import setup, find_packages

setup(
    name='crd',
    version='0.0.2',
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
        'keyring'
    ],
    scripts=['crd/cli.py'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points = {
        'console_scripts': ['crd=crd.cli:main'],
    }
)

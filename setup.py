from setuptools import setup, find_packages

setup(
    name='crd',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/mibarg/crd',
    license='MIT',
    author='mibarg',
    author_email='mibarg@users.noreply.github.com',
    description='desc',
    install_requires=[
        'azure-keyvault',
        'adal',
        'argparse'
    ],
    scripts=['crd/main.py'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)

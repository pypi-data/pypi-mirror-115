from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

# The directory containing this file
# The text of the README file
# with open(path.join( "README.md")) as f:
#     README = f.read()

README = """# Warp

Warp brings Ethereum Virtual Machine to StarkNet, making it possible to run Ethereum [Smart Contracts](https://ethereum.org/en/developers/docs/smart-contracts/) as StarkNet contracts.
"""

all_reqs = ['aiohttp==3.7.4.post0', 'asttokens==2.0.4', 'async-timeout==3.0.1', 'attrs==21.2.0', 'base58==2.1.0', 'bitarray==1.2.2', 'cachetools==4.2.2', 'cairo-lang==0.3.0', 'certifi==2021.5.30', 'chardet==4.0.0', 'charset-normalizer==2.0.3', 'click==8.0.1', 'cytoolz==0.11.0', 'ecdsa==0.17.0', 'eth-abi==2.1.1', 'eth-account==0.5.5', 'eth-hash==0.2.0', 'eth-keyfile==0.5.1', 'eth-keys==0.3.3', 'eth-rlp==0.2.1', 'eth-typing==2.2.2', 'eth-utils==1.9.5', 'fastecdsa==2.2.1', 'frozendict==1.2', 'hexbytes==0.2.1', 'idna==3.2', 'importlib-metadata==4.6.1', 'iniconfig==1.1.1', 'ipfshttpclient==0.7.0', 'jsonschema==3.2.0', 'lark-parser==0.8.5', 'lru-dict==1.1.7', 'marshmallow==3.13.0', 'marshmallow-dataclass==8.4.2', 'marshmallow-enum==1.5.1', 'marshmallow-oneofschema==3.0.1', 'mpmath==1.2.1', 'multiaddr==0.0.9', 'multidict==5.1.0', 'mypy-extensions==0.4.3', 'netaddr==0.8.0', 'numpy==1.21.1', 'packaging==21.0', 'parsimonious==0.8.1', 'pipdeptree==2.0.0', 'pluggy==0.13.1', 'prometheus-client==0.11.0', 'protobuf==3.17.3', 'py==1.10.0', 'py-solc-x==1.1.0', 'pycryptodome==3.10.1', 'pyparsing==2.4.7', 'pyrsistent==0.18.0', 'pytest==6.2.4', 'pytest-asyncio==0.15.1', 'requests==2.26.0', 'rlp==2.0.1', 'semantic-version==2.8.5', 'six==1.16.0', 'sympy==1.8', 'toml==0.10.2', 'toolz==0.11.1', 'typeguard==2.12.1', 'typing-extensions==3.10.0.0', 'typing-inspect==0.7.1', 'urllib3==1.26.6', 'varint==1.0.2', 'vyper==0.2.14', '# Editable install with no version control (warp==0.1.0)', '-e /home/greg/warp/lib/python3.7/site-packages/warp-0.1.0-py3.7.egg', 'web3==5.21.0', 'websockets==9.1', 'yarl==1.6.3', 'zipp==3.5.0', '']
# automatically captured required modules for install_requires in requirements.txt and as well as configure dependency links
# with open(path.join( 'requirements.txt'), encoding='utf-8') as f:
#     all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]

setup (
 name = 'evm-warp',
 description='Transpile EVM-Compatible Languages To Cairo',
 version='0.1.1',
 package_dir={"": "warp"},
 packages=["cli","cli.compilation", "transpiler", "transpiler.Operations"], # list of all packages
 include_package_data=True,
 package_data={'': ['*.json']},
 install_requires=install_requires,
 python_requires='>=3.7', # any python greater than 3.7
 entry_points='''
        [console_scripts]
        warp=cli.warp_cli:main
    ''',
 author="Nethermind",
 keyword="Ethereum, Layer2, ETH, StarkNet, Nethermind, StarkWare, transpilation, warp, transpiler, cairo",
 long_description=README,
 long_description_content_type="text/markdown",
 license='Apache 2.0',
 url='https://github.com/NethermindEth/warp',
 download_url='',
  dependency_links=dependency_links,
  author_email='vardygreg23@gmail.com',
  classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)
# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keypair_kinetic_sdk', 'keypair_kinetic_sdk.keypair']

package_data = \
{'': ['*']}

install_requires = \
['bip-utils>=2.7.0,<3.0.0',
 'pybase64>=1.2.3,<2.0.0',
 'pybip39>=0.1.0,<0.2.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'solana>=0.28.0,<0.29.0']

setup_kwargs = {
    'name': 'keypair-kinetic-sdk',
    'version': '0.1.1',
    'description': '',
    'long_description': 'Hello Wolrd',
    'author': 'Antoni Oktha Fernandes',
    'author_email': '37358597+DesKaOne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

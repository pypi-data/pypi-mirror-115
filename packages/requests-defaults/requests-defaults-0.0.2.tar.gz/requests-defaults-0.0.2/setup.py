# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requests_defaults']

package_data = \
{'': ['*']}

install_requires = \
['pytest-cov>=2.12.1,<3.0.0',
 'pytest-httpserver>=1.0.1,<2.0.0',
 'pytest-mock>=3.6.1,<4.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0']

setup_kwargs = {
    'name': 'requests-defaults',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'Dani Hodovic',
    'author_email': 'dani.hodovic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requests_defaults']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'requests-defaults',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Dani Hodovic',
    'author_email': 'dani.hodovic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

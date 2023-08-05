# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongodm']

package_data = \
{'': ['*']}

install_requires = \
['pymongo>=3.12.0,<4.0.0']

setup_kwargs = {
    'name': 'mongodm',
    'version': '0.1.0',
    'description': 'Simple ODM for MongoDB',
    'long_description': 'mongodm\n',
    'author': 'Deni',
    'author_email': 'azureswastika@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/azureswastika/mongodm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

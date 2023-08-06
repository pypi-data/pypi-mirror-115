# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['syntheticdb']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3', 'pandas>=1', 'scipy>=1', 'sqlparse>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'syntheticdb',
    'version': '0.0.17',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)

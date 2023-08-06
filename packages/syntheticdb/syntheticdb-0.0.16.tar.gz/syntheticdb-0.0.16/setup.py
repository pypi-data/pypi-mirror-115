# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['syntheticdb']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0',
 'pandas>=1.2.1,<2.0.0',
 'scipy>=1',
 'sqlparse>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'syntheticdb',
    'version': '0.0.16',
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

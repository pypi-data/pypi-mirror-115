# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['table2sql']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['table2sql = table2sql.cli:cli']}

setup_kwargs = {
    'name': 'table2sql',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Piotr Gredowski',
    'author_email': 'piotrgredowski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

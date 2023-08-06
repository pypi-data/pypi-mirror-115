# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitrenametool', 'gitrenametool.Utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['gitrename = gitrenametool.cli:cli']}

setup_kwargs = {
    'name': 'gitrenametool',
    'version': '0.0.1',
    'description': 'rename git`s files dirs ',
    'long_description': None,
    'author': 'ArthurWang',
    'author_email': 'yahui9119@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

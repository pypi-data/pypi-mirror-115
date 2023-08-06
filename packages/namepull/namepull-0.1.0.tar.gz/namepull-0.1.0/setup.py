# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['namepull']

package_data = \
{'': ['*']}

install_requires = \
['PyMySQL>=1.0.2,<2.0.0',
 'absl-py>=0.13.0,<0.14.0',
 'aiohttp>=3.7.4,<4.0.0',
 'python-sql>=1.2.2,<2.0.0']

entry_points = \
{'console_scripts': ['namepull = namepull:run']}

setup_kwargs = {
    'name': 'namepull',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Artanicus',
    'author_email': 'artanicus@nocturnal.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

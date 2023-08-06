# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glenv', 'glenv.managers', 'glenv.types']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0', 'pytest>=6.2.4,<7.0.0', 'python-gitlab>=2.9.0,<3.0.0']

entry_points = \
{'console_scripts': ['glenv = glenv.__main__:cli']}

setup_kwargs = {
    'name': 'glenv',
    'version': '0.1.0',
    'description': 'Easily manage your Gitlab CI variables using .env files',
    'long_description': '',
    'author': 'Tiko JG',
    'author_email': 'vjgarcera@gmail.com',
    'maintainer': 'Tiko JG',
    'maintainer_email': 'vjgarcera@gmail.com',
    'url': 'https://vjgarcera.github.io/glenv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['causalenv', 'causalenv.envs']

package_data = \
{'': ['*']}

install_requires = \
['gym>=0.18.0,<0.19.0', 'setuptools>=57.0,<58.0']

setup_kwargs = {
    'name': 'causalenv',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Elias Aoun Durand',
    'author_email': 'elias.aoundurand@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

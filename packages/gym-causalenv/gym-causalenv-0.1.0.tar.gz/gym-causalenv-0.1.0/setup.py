# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gym_causalenv', 'gym_causalenv.envs']

package_data = \
{'': ['*']}

install_requires = \
['gym>=0.0,<0.1']

setup_kwargs = {
    'name': 'gym-causalenv',
    'version': '0.1.0',
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

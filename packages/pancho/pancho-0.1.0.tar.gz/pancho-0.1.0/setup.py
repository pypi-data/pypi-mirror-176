# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pancho',
 'pancho.bootstraping',
 'pancho.definitions',
 'pancho.definitions.contracts',
 'pancho.identity',
 'pancho.interaction',
 'pancho.operations',
 'pancho.processing']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'zorge>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'pancho',
    'version': '0.1.0',
    'description': 'Commands processor',
    'long_description': None,
    'author': 'smairon',
    'author_email': 'man@smairon.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

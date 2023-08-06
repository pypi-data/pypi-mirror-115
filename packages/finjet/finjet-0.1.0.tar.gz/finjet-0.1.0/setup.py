# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['finjet']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'finjet',
    'version': '0.1.0',
    'description': 'Dependency injection like FastAPI.',
    'long_description': None,
    'author': 'elda27',
    'author_email': 'kaz.birdstick@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

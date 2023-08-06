# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['workforce_async']

package_data = \
{'': ['*']}

install_requires = \
['parse>=1.0,<2.0']

setup_kwargs = {
    'name': 'workforce-async',
    'version': '0.9.1',
    'description': 'Asyncio Wrapper',
    'long_description': None,
    'author': 'Caswall Engelsman',
    'author_email': 'mail@cengelsman.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

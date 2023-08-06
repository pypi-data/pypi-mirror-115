# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chatushka', 'chatushka.matchers', 'chatushka.samples', 'chatushka.transports']

package_data = \
{'': ['*']}

install_requires = \
['aiocron>=1.6,<2.0',
 'click>=8.0.1,<9.0.0',
 'httpx>=0.18.2,<0.19.0',
 'pydantic[dotenv]>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'chatushka',
    'version': '0.3.1',
    'description': 'Bot that can make your chat explode!',
    'long_description': '# boombot\n',
    'author': 'Aleksandr Shpak',
    'author_email': 'shpaker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shpaker/chatushka',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

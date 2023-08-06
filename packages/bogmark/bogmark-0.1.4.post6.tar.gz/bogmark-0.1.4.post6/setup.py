# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bogmark',
 'bogmark.bases',
 'bogmark.logger',
 'bogmark.rabbitmq',
 'bogmark.server',
 'bogmark.server.middlewares',
 'bogmark.shared',
 'bogmark.structures']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.7.4,<4.0.0',
 'httpx',
 'msgpack-asgi>=1.1.0,<2.0.0',
 'orjson',
 'pydantic[email]>=1.8.2,<2.0.0',
 'python-dotenv']

extras_require = \
{'all': ['fastapi>=0.68.0,<0.69.0',
         'starlette-prometheus>=0.7.0,<0.8.0',
         'pika>=1.2.0,<2.0.0',
         'aio-pika>=6.8.0,<7.0.0'],
 'rabbitmq': ['pika>=1.2.0,<2.0.0', 'aio-pika>=6.8.0,<7.0.0'],
 'server': ['fastapi>=0.68.0,<0.69.0', 'starlette-prometheus>=0.7.0,<0.8.0']}

setup_kwargs = {
    'name': 'bogmark',
    'version': '0.1.4.post6',
    'description': '',
    'long_description': None,
    'author': 'Bogdan',
    'author_email': 'evstrat.bg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telegram_parser']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0']

entry_points = \
{'console_scripts': ['tp = telegram_parser.cli:run']}

setup_kwargs = {
    'name': 'telegram-parser',
    'version': '0.0.1',
    'description': 'Parse Telegram Bot API',
    'long_description': '# Telegram parser\n\nParse Telegram Bot API to OpenAPI, RAML or use as dataclass\n',
    'author': 'Arwichok',
    'author_email': 'me@arwi.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

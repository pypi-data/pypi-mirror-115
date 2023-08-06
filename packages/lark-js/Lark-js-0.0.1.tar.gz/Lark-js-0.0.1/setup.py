# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lark-js']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'lark-js',
    'version': '0.0.1',
    'description': 'An extension to Lark that generates a Javascript standalone',
    'long_description': '# Lark.js\n\nAn extension to Lark that generates a Javascript standalone\n\n\nWork in progress. Coming soon!',
    'author': 'Erez Shin',
    'author_email': 'erezshin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lark-parser/lark.js',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

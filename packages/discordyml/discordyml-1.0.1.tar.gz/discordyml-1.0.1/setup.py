# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discordyml']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'discordyml',
    'version': '1.0.1',
    'description': 'An easy (but probably inefficient) library to assign data to discord users and guilds using a small subset of YAML',
    'long_description': 'None',
    'author': 'Umar Sharief',
    'author_email': 'umar.sharief04@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

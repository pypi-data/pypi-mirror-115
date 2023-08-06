# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dqp']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'dqp',
    'version': '0.0.1',
    'description': 'A simple library to process a list of messages from disk',
    'long_description': 'Disk Queue Processing\n=====================\n\n\nLibrary to do simple disk based processing of messagepack dictionaries in a file.\n\n',
    'author': 'Bram Neijt',
    'author_email': 'bram@neijt.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bneijt/dqp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

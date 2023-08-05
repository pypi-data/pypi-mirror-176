# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stparser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stparser',
    'version': '0.2.0',
    'description': 'A tool to convert strings to types. Primary use case is type specifications in configuration files.',
    'long_description': None,
    'author': 'Patrick Wells',
    'author_email': 'pwells@ucdavis.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metrics_cleaner']

package_data = \
{'': ['*']}

install_requires = \
['prometheus-client>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'metrics-cleaner',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'westwardharbor0',
    'author_email': 'westwardharbor0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['BETDisk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'flow360-betdisk',
    'version': '0.1.11',
    'description': '',
    'long_description': 'None',
    'author': 'Flexcompute',
    'author_email': 'support@flexcompute.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

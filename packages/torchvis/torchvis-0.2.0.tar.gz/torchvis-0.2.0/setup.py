# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchvis', 'torchvis.selflib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'torchvis',
    'version': '0.2.0',
    'description': 'Pytorch visualization experiments',
    'long_description': None,
    'author': 'Shawn Presser',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

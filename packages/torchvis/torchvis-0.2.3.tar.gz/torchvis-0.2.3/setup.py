# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchvis', 'torchvis.selflib']

package_data = \
{'': ['*']}

install_requires = \
['ansi-escapes>=0.1.1,<0.2.0',
 'ansi-styles>=0.2.2,<0.3.0',
 'supports-color>=0.1.2,<0.2.0']

setup_kwargs = {
    'name': 'torchvis',
    'version': '0.2.3',
    'description': 'Pytorch visualization experiments',
    'long_description': None,
    'author': 'Shawn Presser',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

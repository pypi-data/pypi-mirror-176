# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_scinote']

package_data = \
{'': ['*']}

install_requires = \
['authlib>=1.1.0,<2.0.0', 'httpx>=0.23.0,<0.24.0', 'pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'python-scinote',
    'version': '0.2.6',
    'description': '',
    'long_description': '',
    'author': 'yamshy',
    'author_email': 'shyam.ajudia@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

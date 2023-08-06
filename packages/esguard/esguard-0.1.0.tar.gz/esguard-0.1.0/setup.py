# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['esguard']

package_data = \
{'': ['*']}

install_requires = \
['docker>=5.0.0,<6.0.0', 'elasticsearch>=7.12.1,<8.0.0', 'six>=1.16.0,<2.0.0']

setup_kwargs = {
    'name': 'esguard',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

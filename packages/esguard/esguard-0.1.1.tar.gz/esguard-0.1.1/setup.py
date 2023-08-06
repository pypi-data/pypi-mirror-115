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
    'version': '0.1.1',
    'description': 'esguard provides a Python decorator that waits for processing while monitoring the load of Elasticsearch.',
    'long_description': '# esguard\n\nesguard provides a Python decorator that waits for processing while monitoring the load of Elasticsearch.\n\n## Quick Start\n\nYou need to launch elasticsearch before quick start.\n\n```python\nfrom esguard import ESGuard\n\n\n@ESGuard(os_cpu_percent=90, os_mem_used_percent=-1, jvm_mem_heap_used_percent=-1).decotator()\ndef mock_func(x):\n    return x\n        \nself.assertEqual(mock_func(1), 1)\n```\n\n## Test\n\nYou need to launch elasticsearch before testing.\n\n```sh\n$ docker-compose up -d --build\n$ poetry run pytest\n```\n\n',
    'author': 'po3rin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/po3rin/esguard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

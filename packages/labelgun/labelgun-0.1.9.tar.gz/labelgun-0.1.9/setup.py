# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labelgun', 'labelgun.integrations']

package_data = \
{'': ['*']}

install_requires = \
['aenum>=3.0.0,<4.0.0']

extras_require = \
{'logger': ['python-json-logger>=2.0,<2.1', 'structlog>=20,<22']}

setup_kwargs = {
    'name': 'labelgun',
    'version': '0.1.9',
    'description': 'Library to define system events',
    'long_description': None,
    'author': 'Aleksey Petrunnik',
    'author_email': 'apetrunnik@usetech.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vcard']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil']

setup_kwargs = {
    'name': 'vcard',
    'version': '0.14.0',
    'description': 'vCard validator, class and utility functions',
    'long_description': None,
    'author': 'Victor Engmark',
    'author_email': 'victor@engmark.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

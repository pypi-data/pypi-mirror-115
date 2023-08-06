# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_path_signature']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-path-signature',
    'version': '210809.1',
    'description': '',
    'long_description': None,
    'author': 'TBD',
    'author_email': 'tbd@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

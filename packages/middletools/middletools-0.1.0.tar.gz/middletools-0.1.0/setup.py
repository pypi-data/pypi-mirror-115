# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['middletools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'middletools',
    'version': '0.1.0',
    'description': 'This python library allows you integrate async-await middleware-based system to your project',
    'long_description': None,
    'author': 'deknowny',
    'author_email': 'deknowny@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

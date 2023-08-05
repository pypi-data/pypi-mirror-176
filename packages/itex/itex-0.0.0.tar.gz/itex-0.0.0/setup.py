# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'itex',
    'version': '0.0.0',
    'description': 'iTeX',
    'long_description': None,
    'author': 'iydon',
    'author_email': 'liangiydon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

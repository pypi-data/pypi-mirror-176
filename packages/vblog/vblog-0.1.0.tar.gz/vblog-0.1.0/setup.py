# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vblog']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vblog',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Vincent Berthet',
    'author_email': 'vincent.berthet42@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

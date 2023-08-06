# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textbytesencoder']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'textbytesencoder',
    'version': '0.1.10',
    'description': 'Module encoding and encrypting text by key',
    'long_description': '# textbytesencoder\nModule encoding and encrypting text by key\n',
    'author': 'D1ffic00lt',
    'author_email': 'dm.filinov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/D1ffic00lt/textbytesencoder',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textbytesencoder']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'textbytesencoder',
    'version': '0.1.12',
    'description': 'Module encoding and encrypting text by key',
    'long_description': '# TextBytesEncoder\nModule encoding and encrypting text by key\n## Usage example\n```python\nfrom textbytesencoder import Encoder\n\nencoder = Encoder(key=None, save_key=False)  # key: Optional[bytes] = None, save_key: Optional[bool] = False\nprint(encoder.encrypt(text))  # type(text) == str\nprint(encoder.decrypt(text))  # type(text) == bytes\n```\nDuring initialization, you can specify the optional `key` parameter (key, type and purpose see below) and the optional `save_key` parameter (saves the key to a separate file)\n## Parameters\nParameter `key` of type bytes, generated using the `Fernet.generate_key()` function \nor using the `base64.urlsafe_b64encode(os.urandom(32))` function used to encode or decode text.\n```python\nprint(encoder.key)\n```\n\n```python\nencoder.key = b"key"  # key = Fernet.generate_key() or base64.urlsafe_b64encode(os.urandom(32))\n```',
    'author': 'D1ffic00lt',
    'author_email': 'dm.filinov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/D1ffic00lt/textbytesencoder',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysignalclijsonrpc']

package_data = \
{'': ['*']}

install_requires = \
['python-magic>=0.4.27,<0.5.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pysignalclijsonrpc',
    'version': '22.11.6',
    'description': 'Python API client for signal-cli JSON-RPC',
    'long_description': '# pysignalclijsonrpc - Python API client for signal-cli JSON-RPC\n',
    'author': 'Stefan Heitmüller',
    'author_email': 'stefan.heitmueller@gmx.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/morph027/pysignalclijsonrpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

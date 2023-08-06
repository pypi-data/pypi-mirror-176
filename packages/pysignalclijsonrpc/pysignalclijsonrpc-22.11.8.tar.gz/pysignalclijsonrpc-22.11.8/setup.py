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
    'version': '22.11.8',
    'description': 'Python API client for signal-cli JSON-RPC',
    'long_description': '# pysignalclijsonrpc - Python API client for signal-cli JSON-RPC\n\nPython client for [signal-cli 0.11.5+](https://github.com/AsamK/signal-cli/blob/master/CHANGELOG.md#0115---2022-11-07) native HTTP endpoint for JSON-RPC methods.\n\n## Installation\n\n```bash\npip install pysignalclijsonrpc\n```\n\n## Usage\n\n### Initalization\n\n#### Default\n\n```python\nfrom pysignalclijsonrpc.api import SignalCliJSONRPCApi\n\nsignal_cli_rest_api = SignalCliJSONRPCApi(\n    endpoint="http://localhost:3000/api/v1/rpc",\n    account="+1234567890" # one of your registered signal-cli accounts\n)\n```\n\n#### Basic authentication\n\n```python\nfrom pysignalclijsonrpc.api import SignalCliJSONRPCApi\n\nsignal_cli_rest_api = SignalCliJSONRPCApi(\n    endpoint="http://localhost:8080/api/v1/rpc",\n    account="+1234567890",\n    auth=("user", "password")\n)\n```\n\n#### HTTPS w/ self-signed certificates\n\n```python\nfrom pysignalclijsonrpc.api import SignalCliJSONRPCApi\n\nsignal_cli_rest_api = SignalCliJSONRPCApi(\n    endpoint="https://localhost:8443/api/v1/rpc",\n    account="+1234567890",\n    verify_ssl=False\n)\n```\n\n### Send message\n\n#### Plain text message\n\n```python\nsignal_cli_rest_api.send_message("Test")\n```\n\n#### Plain text message w/ attachment from file\n\n```python\nsignal_cli_rest_api.send_message("Test", filenames=["/tmp/some-image.png"])\n```\n',
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

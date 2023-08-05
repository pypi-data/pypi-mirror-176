# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scamadviser_client', 'scamadviser_client.schema']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'scamadviser-client',
    'version': '0.1.2',
    'description': 'A python SDK for ScamAdviser API',
    'long_description': '## Installation\n\n```\npip install scamadviser_client\n```\n\nor\n\n```\npoetry add scamadviser_client\n```\n\n## Usage\n\n```python\nfrom scamadviser_client import FeedAPI\n\napi = FeedAPI(apikey=[your_apikey])\n\napi.list(params={"type": "daily"})\napi.download(params={"path": "/5-minute/1602245968.json"})\n```\n\n## Development\n\nYou may install [Nix](https://nixos.org/download.html) to have fully env settings by running `nix-shell`,\nor simply use `poetry shell` to bootstrap this package if you would like to join our development.\n\nWe also use [justfile](https://github.com/casey/just) to provide some simple commands, you may use\n\n```bash\njust default\n```\n\nto check all of these available commands.\n\n### start the environment (poetry)\n\n```bash\njust up\n```\n\n### stop the environment (poetry)\n\n```bash\njust down\n```\n\n### test\n\n```bash\njust test\n```\n\n### make the code prettier\n\n```bash\njust be-pretty\n```\n',
    'author': 'Carol H',
    'author_email': 'sheseee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gogolook-Inc/scamadviser_client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

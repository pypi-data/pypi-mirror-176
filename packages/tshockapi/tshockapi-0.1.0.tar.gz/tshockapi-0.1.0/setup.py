# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tshockapi']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'tshockapi',
    'version': '0.1.0',
    'description': 'Quick access to TShock REST API using python.',
    'long_description': 'Quick access to TShock REST API using python.\n\n## Example\n\n```python\nimport tshockapi  # Import the tshockapi module\n\nserver = tshockapi.Server(host="127.0.0.1", port=7878, token="1234567890")  # Create a server object\nprint(server.v3_server_rawcmd(cmd="/who"))  # Print the result of the /who command\n# {\'status\': \'200\', \'response\': [\'There are currently no players online.\']}\n',
    'author': 'Qianyiovo',
    'author_email': 'qianyiovo@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

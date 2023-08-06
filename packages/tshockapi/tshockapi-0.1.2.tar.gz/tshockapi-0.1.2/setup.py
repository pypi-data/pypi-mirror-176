# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tshockapi']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'tshockapi',
    'version': '0.1.2',
    'description': 'Quick access to TShock REST API using python.',
    'long_description': 'Quick access to TShock REST API using python.\n\n## Endpoints\n\n<details>\n\n<summary>Server</summary>\n\n/status\n\n/tokentest\n\n/v2/token/create\n\n/v2/server/broadcast\n\n/v3/server/rawcmd\n\n/v3/server/motd\n\n/v2/server/off\n\n/v3/server/reload\n\n/v3/server/rules\n\n/v2/server/status\n\n</details>\n\n<details>\n\n<summary>User</summary>\n\n/v2/users/create\n\n/v2/users/destroy\n\n/v2/users/read\n\n/v2/users/list\n\n/v2/users/update\n\n/v2/users/activelist\n\n</details>\n\n<details>\n\n<summary>World</summary>\n\n/v3/world/bloodmoon\n\n/v2/world/butcher\n\n/world/meteor\n\n/world/read\n\n/v2/world/save\n\n</details>\n\n<details>\n\n<summary>Ban</summary>\n\n/v3/bans/create\n\n/v3/bans/destroy\n\n/v3/bans/read\n\n/v3/bans/list\n\n</details>\n\n<details>\n\n<summary>Player</summary>\n\n/v2/players/kick\n\n/v2/players/kill\n\n/v2/players/list\n\n/v2/players/mute\n\n/v4/players/read\n\n/v2/players/unmute\n\n</details>\n\n## Example\n\n```python\nimport tshockapi  # Import the tshockapi module\n\nserver = tshockapi.Server(host="127.0.0.1", port=7878, token="1234567890")  # Create a server object\nprint(server.v3_server_rawcmd(cmd="/who"))  # Print the result of the /who command\n# {\'status\': \'200\', \'response\': [\'There are currently no players online.\']}\n```\n\n## Installation\n\n### Windows\n\n```bash\npip install tshockapi\n```\n\n### Linux\n\n```bash\npip3 install tshockapi\n```',
    'author': 'Qianyiovo',
    'author_email': 'qianyiovo@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

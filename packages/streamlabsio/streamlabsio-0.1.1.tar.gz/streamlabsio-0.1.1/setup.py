# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlabsio']

package_data = \
{'': ['*']}

install_requires = \
['observable>=1.0.3,<2.0.0',
 'python-engineio==3.14.2',
 'python-socketio[client]==4.6.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

setup_kwargs = {
    'name': 'streamlabsio',
    'version': '0.1.1',
    'description': 'Get real time Twitch/Youtube events through Streamlabs SocketIO API',
    'long_description': '[![PyPI version](https://badge.fury.io/py/streamlabsio.svg)](https://badge.fury.io/py/streamlabsio)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/onyx-and-iris/streamlabs-socketio-py/blob/dev/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n# A Python client for Streamlabs SocketIO API\n\n### Requirements\n\n-   A Streamlabs SocketIO API key.\n    -   You can acquire this by logging into your Streamlabs.com dashboard then `Settings->Api Settings->API Tokens`\n\n### How to install using pip\n\n```\npip install streamlabsio\n```\n\n### How to Use\n\nYou may store your api key in a `config.toml` file, its contents should resemble:\n\n```toml\n[streamlabs]\ntoken = "<apikey>"\n```\n\nPlace it next to your `__main__.py` file.\n\n#### Otherwise:\n\nYou may pass it as a keyword argument.\n\nExample `__main__.py`:\n\n```python\nfrom threading import Thread\n\nimport streamlabsio\n\n\ndef on_twitch_event(event, msg):\n    print(f"{event}: {msg.attrs()}")\n\n\ndef register_callbacks(client):\n    client.obs.on("streamlabs", on_twitch_event)\n    client.obs.on("twitch_account", on_twitch_event)\n\n\ndef main():\n    with streamlabsio.connect(token="<apikey>") as client:\n        worker = Thread(target=register_callbacks, args=(client,), daemon=True)\n        worker.start()\n\n        while cmd := input("<Enter> to exit\\n"):\n            if not cmd:\n                break\n\n\nif __name__ == "__main__":\n    main()\n```\n\n### Attributes\n\nFor event messages you may inspect the available attributes using `attrs()`.\n\nexample:\n\n```python\ndef on_twitch_event(event, msg):\n    print(f"{event}: {msg.attrs()}")\n```\n\n### Official Documentation\n\n-   [Streamlabs SocketIO API](https://dev.streamlabs.com/docs/socket-api)\n',
    'author': 'onyx-and-iris',
    'author_email': 'code@onyxandiris.online',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/onyx-and-iris/streamlabs-socketio-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

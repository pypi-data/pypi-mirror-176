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
    'version': '0.1.0',
    'description': 'Get real time Twitch/Youtube events through Streamlabs SocketIO API',
    'long_description': None,
    'author': 'onyx-and-iris',
    'author_email': 'code@onyxandiris.online',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

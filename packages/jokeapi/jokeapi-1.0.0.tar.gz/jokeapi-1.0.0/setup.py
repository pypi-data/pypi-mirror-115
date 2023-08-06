# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jokeapi']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'simplejson>=3.17.2,<4.0.0', 'urllib3>=1.26.2,<2.0.0']

setup_kwargs = {
    'name': 'jokeapi',
    'version': '1.0.0',
    'description': "Python API Wrapper for Sv443's JokeAPI (https://v2.jokeapi.dev)",
    'long_description': None,
    'author': 'thenamesweretakenalready',
    'author_email': '43702423+thenamesweretakenalready@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

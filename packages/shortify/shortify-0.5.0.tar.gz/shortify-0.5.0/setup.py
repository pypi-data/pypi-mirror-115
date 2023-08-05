# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shortify', 'shortify.main', 'shortify.services']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.26.0']

entry_points = \
{'console_scripts': ['shortify = shortify.__main__:main']}

setup_kwargs = {
    'name': 'shortify',
    'version': '0.5.0',
    'description': 'A simple URL-shortening library with CLI support.',
    'long_description': '<h1 align="center">\n    Shortify - shorten your URL\n</h1>\n\nA simple URL shortening API wrapper library written in Python by Dositan.\n\n## Supported services\n1. [TinyURL](https://tinyurl.com)\n2. [Git.io](https://git.io)\n3. [Shrtco.de](https://shrtco.de)\n4. [Is.gd](is.gd)\n5. [Clck.ru](clck.ru)\n\n-----\n\n## Installing\n```console\n$ pip install shortify\n\n---> 100%\n```\n\nAfter pressing enter, pip will install all the required packages for the project.\n\n</div>\n\n-----\n\n## CLI usage\nLike all CLIs, `shortify` supports `--help` flag.\n```console\n$ shortify --help\n\nusage: shortify [-h] {tinyurl,git} url\n\nShortify CLI!\n\n.....\n```\n\nGenerating a shortened URL using git.io:\n```console\n$ shortify git https://www.github.com/Dositan/Boribay/\n\nhttps://git.io/JBsPu\n```\n',
    'author': 'Dastan Ozgeldi',
    'author_email': 'ozgdastan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dositan/shortify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clicom']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'clicom',
    'version': '0.0.1',
    'description': '',
    'long_description': 'This package wraps [`Typer`](https://typer.tiangolo.com/) library and adds the ability to run your commands in a loop,\nexecuting commands one after the other until tying `exit` or invoking keyboard interrupt. ',
    'author': 'limonyellow',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

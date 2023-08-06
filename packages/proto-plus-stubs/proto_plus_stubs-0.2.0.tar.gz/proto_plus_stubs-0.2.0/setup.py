# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proto-stubs']

package_data = \
{'': ['*'],
 'proto-stubs': ['marshal/*', 'marshal/collections/*', 'marshal/rules/*']}

install_requires = \
['proto-plus>=1.18.0', 'types-protobuf>=3.17.4']

setup_kwargs = {
    'name': 'proto-plus-stubs',
    'version': '0.2.0',
    'description': 'Type stubs for proto-plus',
    'long_description': '# Type stubs for proto-plus-stubs\n[![PyPI version](https://badge.fury.io/py/proto-plus-stubs.svg)](https://badge.fury.io/py/proto-plus-stubs)\n\nThis package provides type stubs for the [proto-plus](https://pypi.org/project/proto-plus/) package.\n\n**This is in no way affiliated with Google.**\n\nThe stubs were created automatically by [stubgen](https://mypy.readthedocs.io/en/stable/stubgen.html).\n## Installation\n```shell script\n$ pip install proto-plus-stubs\n```\n',
    'author': 'Henrik Bruåsdal',
    'author_email': 'henrik.bruasdal@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/henribru/proto-plus-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

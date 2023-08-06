# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['termcolor_util']

package_data = \
{'': ['*']}

install_requires = \
['termcolor>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'termcolor-util',
    'version': '2022.11.1',
    'description': 'wrapper functions over termcolor',
    'long_description': '`termcolor_util` is a set of functions on top of termcolor for every\nsingle color.\n\nInstallation\n============\n\n    pip install termcolor_util\n\nFunctions\n=========\n\n    def yellow(text: str, bold=False, underline=False) -> str: ...\n\n    def green(text: str, bold=False, underline=False) -> str: ...\n\n    def blue(text: str, bold=False, underline=False) -> str: ...\n\n    def red(text: str, bold=False, underline=False) -> str: ...\n\n    def gray(text: str, bold=False, underline=False) -> str: ...\n\n    def cyan(text: str, bold=False, underline=False) -> str: ...\n\n    def magenta(text: str, bold=False, underline=False) -> str: ...\n\n    def white(text: str, bold=False, underline=False) -> str: ...\n\nBeside colors, there is a function for directly printing on the stderr.\n\n    def eprint(*args) -> None: ...\n',
    'author': 'Bogdan Mustiata',
    'author_email': 'bogdan.mustiata@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)

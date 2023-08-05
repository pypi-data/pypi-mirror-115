# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['piglatincli']
install_requires = \
['click-help-colors>=0.9.1,<0.10.0', 'click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['plcli = piglatincli:main']}

setup_kwargs = {
    'name': 'piglatincli',
    'version': '0.1.0',
    'description': 'A cli to convert English to pig latin and vice versa',
    'long_description': '',
    'author': 'Avanindra Chakraborty',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AvanindraC/Pig-Latin-Cli',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sha_assist']
install_requires = \
['click>=8.0.1,<9.0.0']

setup_kwargs = {
    'name': 'sha-assist',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'AndrewGlago',
    'author_email': 'andrewglago1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

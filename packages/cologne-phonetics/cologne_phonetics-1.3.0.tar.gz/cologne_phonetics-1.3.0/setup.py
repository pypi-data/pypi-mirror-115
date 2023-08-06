# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cologne_phonetics']
setup_kwargs = {
    'name': 'cologne-phonetics',
    'version': '1.3.0',
    'description': 'Python implementation of the cologne-phonetics algorithm',
    'long_description': None,
    'author': 'Janek Nouvertné',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)

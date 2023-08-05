# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pynumwork']
setup_kwargs = {
    'name': 'pynumwork',
    'version': '0.1.21',
    'description': 'A Python package that is created for solving simple math problems. Created just for fun :)',
    'long_description': 'Dedicated to Ksenia :)\n\nA simple Python package for simple math operations.\n',
    'author': 'spacecultengineer',
    'author_email': 'spacecultengineer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

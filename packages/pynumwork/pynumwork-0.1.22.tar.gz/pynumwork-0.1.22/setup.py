# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pynumwork']
setup_kwargs = {
    'name': 'pynumwork',
    'version': '0.1.22',
    'description': 'Dedicated to Ksenia @milkpink_2 :)',
    'long_description': 'Dedicated to Ksenia @milkpink_2 :)\n\nA simple Python package for simple math operations.\n',
    'author': 'spacecultengineer',
    'author_email': 'spacecultengineer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

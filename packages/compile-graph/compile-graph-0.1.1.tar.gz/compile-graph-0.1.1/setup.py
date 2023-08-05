# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['compile_graph']
install_requires = \
['docopt>=0.6.2,<0.7.0', 'graphviz>=0.17,<0.18', 'watchdog>=2.1.3,<3.0.0']

entry_points = \
{'compile-graph': ['main = compile_graph:main']}

setup_kwargs = {
    'name': 'compile-graph',
    'version': '0.1.1',
    'description': 'Interactive graph to demonstrate stages of compilation',
    'long_description': None,
    'author': 'Kevin Lai',
    'author_email': 'zlnh4@umsystem.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

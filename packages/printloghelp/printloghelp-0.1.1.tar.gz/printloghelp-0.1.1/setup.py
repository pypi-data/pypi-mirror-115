# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['printloghelp']
install_requires = \
['colorama>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'printloghelp',
    'version': '0.1.1',
    'description': 'ConsoleLog.info(text) or error(text) or warning(text)',
    'long_description': None,
    'author': 'fab4key',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

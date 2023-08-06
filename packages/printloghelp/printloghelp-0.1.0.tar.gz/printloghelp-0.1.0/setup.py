# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['printloghelp']
setup_kwargs = {
    'name': 'printloghelp',
    'version': '0.1.0',
    'description': 'ConsoleLog.info(text) or error(text) or warning(text)',
    'long_description': None,
    'author': 'fab4key',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

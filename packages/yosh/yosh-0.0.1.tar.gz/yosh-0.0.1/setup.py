# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['yosh']
setup_kwargs = {
    'name': 'yosh',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'alibek_akmalovich',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

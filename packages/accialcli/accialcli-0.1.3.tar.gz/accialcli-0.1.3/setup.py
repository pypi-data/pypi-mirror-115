# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['entry']
install_requires = \
['click>=8.0.1,<9.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['accialcli = entry:main']}

setup_kwargs = {
    'name': 'accialcli',
    'version': '0.1.3',
    'description': 'CLI that send to our API 1 Borrower, 1 Application, 1 Loan and 1 Payment',
    'long_description': None,
    'author': 'yud-cumba',
    'author_email': 'yudith.cumba@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

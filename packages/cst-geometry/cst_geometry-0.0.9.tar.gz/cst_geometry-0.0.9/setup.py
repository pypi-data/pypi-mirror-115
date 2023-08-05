# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cst_geometry']

package_data = \
{'': ['*'], 'cst_geometry': ['basic_script/*']}

setup_kwargs = {
    'name': 'cst-geometry',
    'version': '0.0.9',
    'description': 'Package for modelling in CST Microwave studio using python',
    'long_description': None,
    'author': 'konstantgr',
    'author_email': '60608301+konstantgr@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cst_geometry']

package_data = \
{'': ['*'], 'cst_geometry': ['basic_script/*']}

install_requires = \
['numpy>=1.21.1,<2.0.0']

setup_kwargs = {
    'name': 'cst-geometry',
    'version': '0.0.3',
    'description': 'Package for modelling in CST Microwave studio using python',
    'long_description': None,
    'author': 'konstantgr',
    'author_email': '60608301+konstantgr@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

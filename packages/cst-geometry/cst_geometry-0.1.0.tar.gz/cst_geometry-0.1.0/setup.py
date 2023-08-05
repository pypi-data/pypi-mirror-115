# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cst_geometry']

package_data = \
{'': ['*'], 'cst_geometry': ['basic_script/*']}

setup_kwargs = {
    'name': 'cst-geometry',
    'version': '0.1.0',
    'description': 'Package for modeling in CST Microwave studio using python',
    'long_description': 'CST geometry manager\n====================\n\nIt\'s a package that allows you to model geometries contain wires and\nthen export it into CST Microwave Studio project using python.\n\nFeatures\n--------\n\n-  One file format for all wire geometries\n-  Сreating a CST project directly from a script or notebook.\n-  Convenient data structure for creating your own unique complex\n   geometries from wires\n\nUsage\n-----\n\n.. code:: python\n\n    # Path to CST DESIGN ENVIRONMENT.exe\n    path_to_CST_DE = "Absolute\\Path\\To\\CST DESIGN ENVIRONMENT.exe"\n\n\n    def circular_geometry_equal_wires(length, number_of_wires, radius):\n        lengths = [length for i in range(number_of_wires)]\n\n        circular_geometry = simple_geometries.get_circular_geometry(\n            radius=radius, lengths_of_wires=lengths\n        )\n        return circular_geometry\n\n\n    circular_geometry = circular_geometry_equal_wires(2, 4, 4)\n    circular_geometry.create_cst_project(\n        name=\'circular_geometry\',\n        path_to_CST_DE=path_to_CST_DE\n    )\n\nThis code creates simple geometry contain 4 wires equally distributed on\nimaginary cylinder. Then ``create_cst_project`` method creates project.\nTo start using scripts firstly need to change ``path_to_CST_DE``\nvariable. CST project create in cst\\_project folder.\n\nDuring using scripts or notebooks for creating projects all the CST Microwave studio windows must be closed\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nExamples\n--------\n\nSeveral examples located in notebooks folder.\n``make_geometries_example.ipynb`` shows how create sinmple geometries\nusing ``Wire`` and ``Geometry`` classes. ``export_to_cst_example.ipynb``\nshows how create a CST project using jupyter notebook. In ``examples``\nalso located a script shows how create a CST project without using\njupyter notebook.\n\n\\`\n',
    'author': 'konstantgr',
    'author_email': 'konstantin.grotov@metalab.ifmo.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/konstantgr/cst_geometry_manager',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

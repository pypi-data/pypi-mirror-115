# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cst_geometry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cst-geometry',
    'version': '0.1.3',
    'description': 'Package for modeling in CST Microwave studio using python',
    'long_description': 'CST geometry manager\n====================\n\nIt\'s a package that allows you to model geometries contain wires and\nthen export it into CST Microwave Studio project using python.\n\nFeatures\n--------\n\n-  One file format for all wire geometries\n-  Сreating a CST project directly from a script or notebook.\n-  Convenient data structure for creating your own unique complex\n   geometries from wires\n\nInstall\n=======\nFor simple installation use pip: \n::\n\n   pip install cst-geometry\n\n\nUsage\n-----\n\nDuring using scripts or notebooks for creating projects all the CST Microwave studio windows must be closed\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nTo create your own geometry use ``Wire`` and ``Geometry`` classes. ``Wire`` object initializing using start point ``r0``, finish point ``r1`` and its radius. Geometry object initializing using array of ``Wires`` objects. ``Geometry`` object has methods ``export_geometry`` for export .txt file and ``create_cst_project`` for creating project in CST Microwave Studio.\n\n.. code:: python\n\n    import numpy as np\n    from cst_geometry import Wire, Geometry\n\n\n      def get_circular_geometry(radius, lengths_of_wires, wire_radius=1e-3, delta_angle=0):\n          number_of_wires = len(lengths_of_wires)\n          angles = np.linspace(0, 2 * np.pi, number_of_wires, endpoint=False) + delta_angle\n\n          wires = []\n          for i, length in enumerate(lengths_of_wires):\n              phi = angles[i]\n              wire = Wire(\n                  r0=(radius * np.cos(phi), radius * np.sin(phi), -length / 2),\n                  r=(radius * np.cos(phi), radius * np.sin(phi), length / 2),\n                  radius=wire_radius\n              )\n              wires.append(wire)\n\n          return Geometry(wires)\n\nExamples\n--------\n\n.. code:: python\n\n    # Path to CST DESIGN ENVIRONMENT.exe\n    path_to_CST_DE = "Absolute\\Path\\To\\CST DESIGN ENVIRONMENT.exe"\n\n    # Route to folder with .txt geometries and CST projects\n    route_to_folder = "Absolute\\Path\\To\\FOLDER"\n\n\n    def circular_geometry_equal_wires(length, number_of_wires, radius):\n    \tlengths = [length for i in range(number_of_wires)]\n\n    \tcircular_geometry = simple_geometries.get_circular_geometry(\n        \t\tradius=radius, lengths_of_wires=lengths, wire_radius=1e-3, delta_angle=0\n    \t)\n    \treturn circular_geometry\n\n\n    # Creating an array of 18 vertical aligned wires with length 2\n    # on of imaginary cylinder with radius 4\n    circular_geometry = circular_geometry_equal_wires(2, 18, 4)\n    output = circular_geometry.create_cst_project(\n        name="circular_geometry",\n        path_to_CST_DE=path_to_CST_DE,\n        path_to_geometry_folder=route_to_folder,\n        path_to_CST_project=route_to_folder\n    )\n\n\nThis code creates simple geometry contain 18 wires equally distributed on\nimaginary cylinder. Then ``create_cst_project`` method creates project.\nTo start using scripts firstly need to change ``path_to_CST_DE``\nvariable. CST project create in cst\\_project folder.\n\n\n.. image:: examples/CST_example.gif\n\nSeveral examples with CST projects are located in ``examples/`` folder.\n\n\n',
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

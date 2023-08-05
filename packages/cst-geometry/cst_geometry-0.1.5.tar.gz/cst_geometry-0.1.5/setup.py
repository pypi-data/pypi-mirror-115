# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cst_geometry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cst-geometry',
    'version': '0.1.5',
    'description': 'Package for modeling in CST Microwave studio using python',
    'long_description': 'CST geometry manager\n====================\n\nIt\'s a package that allows you to model geometries contain wires and\nthen export it into CST Microwave Studio 2021 project using python.\n\nFeatures\n--------\n\n-  One file format for all wire geometries\n-  Сreate a CST project directly from a script or notebook.\n-  Convenient data structure for creating your own unique complex\n   geometries from wires\n\nInstall\n=======\nFor simple installation use pip: \n::\n\n   pip install cst-geometry\n\n\nUsage\n-----\n\nDuring using scripts or notebooks for creating projects all the CST Microwave studio windows must be closed\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\nWire\n------------------\n\n``Wire`` objects serves to create ``Geometry`` objects. Wire object initialized using start point of wire ``point0``, finish point of wire ``point1`` and its radius ``radius``. As needed after initializing you can use ``length`` property. ``point0`` and ``point1`` are vectors of cartesian coordinates.\n\n.. code:: python\n\n   from cst_geometry import Wire\n\n   x0 = 0; y0 = 0; z0 = 0\n   x1 = 1; y1 = 1; z1 = 1\n   radius = 0.5\n   \n   wire = Wire(\n      point0 = (x0, y0, z0),\n      point1 = (x1, y1, z1),\n      radius = radius\n   )\n   print(wire.length)  # Returns length of wire\n\n\nGeometry\n------------------\n``Geometry`` object allows to easily export geometry to CST Microwave Studio or just export .txt file with geometry parameters. For initializing ``Geometry`` object you should pass a list of ``Wire`` objects. ``create_cst_project`` is a method for creating a .cst project with geometry model. ``export_geometry`` is a method for exporting geometry as .txt file.\n\n.. code:: python\n\n   from cst_geometry import Wire, Geometry\n\n\n   def create_wires_by_rule():\n       wires = []\n       # ...\n       # Your code for creating Wire objects\n       # ...\n       wires.append(wire)\n       return wires\n       \n   wires = create_wires_by_rule()\n   geometry = geometry(wires)\n   \n   \nTo create your own geometry use ``Wire`` and ``Geometry`` classes.\n\n.. code:: python\n\n   import numpy as np\n   from cst_geometry import Wire, Geometry\n\n\n   def get_circular_geometry(radius, lengths_of_wires, wire_radius=1e-3, delta_angle=0):\n       number_of_wires = len(lengths_of_wires)\n       angles = np.linspace(0, 2 * np.pi, number_of_wires, endpoint=False) + delta_angle\n\n       wires = []\n       for i, length in enumerate(lengths_of_wires):\n           phi = angles[i]\n           wire = Wire(\n               point0=(radius * np.cos(phi), radius * np.sin(phi), -length / 2),\n               point1=(radius * np.cos(phi), radius * np.sin(phi), length / 2),\n               radius=wire_radius\n           )\n           wires.append(wire)\n\n       return Geometry(wires)\n\nExamples\n--------\n\n.. code:: python\n   \n    from cst_geometry import simple_geometries\n    \n    # Path to CST DESIGN ENVIRONMENT.exe\n    path_to_CST_DE = r"Absolute\\Path\\To\\CST DESIGN ENVIRONMENT.exe"\n   \n    # Route to folder with .txt geometries and CST projects\n    route_to_folder = r"Absolute\\Path\\To\\FOLDER"\n\n\n    def circular_geometry_equal_wires(length, number_of_wires, radius):\n    \tlengths = [length for i in range(number_of_wires)]\n\n    \tcircular_geometry = simple_geometries.get_circular_geometry(\n        \t\tradius=radius, lengths_of_wires=lengths, wire_radius=1e-3, delta_angle=0\n    \t)\n    \treturn circular_geometry\n\n    # During using scripts or notebooks for creating projects \n    # all the CST Microwave studio windows must be closed !!!\n    \n    # Creating an array of 18 vertical aligned wires with length 2\n    # on of imaginary cylinder with radius 4\n    circular_geometry = circular_geometry_equal_wires(2, 18, 4)\n    output = circular_geometry.create_cst_project(\n        name="circular_geometry",\n        path_to_CST_DE=path_to_CST_DE,\n        path_to_geometry_folder=route_to_folder,\n        path_to_CST_project=route_to_folder\n    )\n\n\nThis code creates simple geometry contain 18 wires equally distributed on\nimaginary cylinder. Then ``create_cst_project`` method creates project.\nTo start using scripts firstly need to change ``path_to_CST_DE``\nvariable. CST project create in cst\\_project folder.\n\n\n.. image:: examples/CST_example.gif\n\nSeveral examples with CST projects are located in ``examples/`` folder.\n\n\n',
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

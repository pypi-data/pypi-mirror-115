# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yupiwrap']

package_data = \
{'': ['*']}

install_requires = \
['tracktable>=1.5.0,<2.0.0', 'traja>=0.2.8,<0.3.0', 'yupi>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'yupiwrap',
    'version': '0.1.1',
    'description': '',
    'long_description': '# yupiwrap\n\nThis repository contains functions to simplify the conversion of Trajectory data\namong [yupi](https://yupi.readthedocs.io/en/latest/) and other useful software libraries designed for analyzing trajectories.\n\nStanding for *Yet Underused Path Instruments*, [yupi](https://yupi.readthedocs.io/en/latest/) is a set of tools designed for collecting, generating and processing trajectory data. The structure of yupi aims to standardize the usage and storage of general purpose trajectories independently of its dimensions. We believe it is useful to be able to convert, when possible, yupi trajectories to the data structures used by other libraries to\nempower our users with the tools offered by third parties. With the same spirit, we offer the possibility of converting data from other libraries to yupi trajectories.\n\n## Installation\n\nCurrent recommended installation method is via the pypi package:\n\n```cmd\npip install yupiwrap\n```\n\nIt will install required dependencies such as [yupi package](https://pypi.org/project/yupi/) from pypi.\n\n## Compatible libraries\n\n### traja\n\nThe [Traja Python package](https://traja.readthedocs.io/en/latest/index.html) is a toolkit for the numerical characterization and analysis of the trajectories of moving animals. It provides several machine learning tools that are not yet implemented in yupi. Even when it is limited to two-dimensional trajectories, there are many resources that traja can offer when dealing with 2D Trajectories in [yupi](https://yupi.readthedocs.io/en/latest/).\n\n#### Converting a *yupi.Trajectory* into a *traja DataFrame*\n\nLet\'s create a trajectory with yupi:\n\n```python\nfrom yupi import Trajectory\n\nx = [0, 1.0, 0.63, -0.37, -1.24, -1.5, -1.08, -0.19, 0.82, 1.63, 1.99, 1.85]\ny = [0, 0, 0.98, 1.24, 0.69, -0.3, -1.23, -1.72, -1.63, -1.01, -0.06, 0.94]\n\ntrack = Trajectory(x=x, y=y, traj_id="Spiral")\n```\n\nWe can convert it to a traja DataFrame simply by:\n\n```python\nfrom yupiwrap import yupi2traja\n\ntraja_track = yupi2traja(track)\n```\n\n⚠️ Only *yupi.Trajectory* objects with two dimensions can be converted to *traja DataFrame* due to traja limitations.\n\n#### Converting a *traja DataFrame* into a *yupi.Trajectory*\n\nIf you have a *traja DataFrame* you can always convert it to a *yupi.Trajectory* by using:\n\n```python\nfrom yupiwrap import traja2yupi\n\nyupi_track = traja2yupi(traja_track)\n```\n\n### tracktable\n\n[Tracktable](https://github.com/sandialabs/tracktable) provides a set of tools for handling 2D and 3D trajectories as well as Terrain trajectories. The core data structures and algorithms on this package are implemented in C++ for speed and more efficient memory use.\n\n#### Converting a *yupi.Trajectory* into a tracktable trajectory\n\nLet\'s create a trajectory with yupi:\n\n```python\nfrom yupiwrap.tracktable import yupi2tracktable, tracktable2yupi\nfrom yupi import Trajectory\n\n# Creating a yupi trajectory representing terrain coordinates\npoints = [[-82.359415, 23.135012],[-82.382116, 23.136252]]\ntrack_1 = Trajectory(points=points, traj_id="ter_track")\n\n# Creating a 2D yupi trajectory\npoints = [[0, 0], [1.0, 0], [0.63, 0.98], [-0.37, 1.24], [-1.24, 0.69],\n          [-1.5, -0.3], [-1.08, -1.23], [-0.19, -1.72], [0.82, -1.63],\n          [1.63, -1.01], [1.99, -0.06], [1.85, 0.94]]\ntrack_2 = Trajectory(points=points, traj_id="2d_track")\n\n# Creating a 3D yupi trajectory\npoints = [[0,0,0], [1,1,3], [3,2,5]]\ntrack_3 = Trajectory(points=points, traj_id="3d_track")\n```\n\nWe can convert these tracks to tracktable trajectories simply by:\n\n```python\ntracktable_track_1 = yupi2tracktable(track_1, is_terrestrial=True)\ntracktable_track_2 = yupi2tracktable(track_2)\ntracktable_track_3 = yupi2tracktable(track_3)\n```\n\n⚠️ If a 3D yupi trajectory is converted to a tracktable trajectory with `is_terrestrial=True` then the `z` axis values are stored as a property called `\'altitude\'` for each point.\n\n⚠️ Only *yupi.Trajectory* objects with two or three dimensions can be converted to tracktable trajectories due to tracktable limitations.\n\n#### Converting a tracktable trajectory into a *yupi.Trajectory*\n\nIf you have a tracktable trajectory you can always convert it to a *yupi.Trajectory* by using:\n\n```python\n# Converting the trajectory from tracktable to yupi\nyupi_track_1 = tracktable2yupi(tracktable_track_1)\n```\n',
    'author': 'Gustavo Viera-López',
    'author_email': 'gvieralopez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

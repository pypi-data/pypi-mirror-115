# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yupiwrap']

package_data = \
{'': ['*']}

install_requires = \
['traja>=0.2.8,<0.3.0', 'yupi>=0.5.7,<0.6.0']

setup_kwargs = {
    'name': 'yupiwrap',
    'version': '0.1.0',
    'description': '',
    'long_description': '# yupiwrap\n\nThis repository contains functions to simplify the conversion of Trajectory data\namong [yupi](https://yupi.readthedocs.io/en/latest/) and other useful software libraries designed for analyzing trajectories.\n\nStanding for *Yet Underused Path Instruments*, [yupi](https://yupi.readthedocs.io/en/latest/) is a set of tools designed for collecting, generating and processing trajectory data. The structure of yupi aims to standardize the usage and storage of general purpose trajectories independently of its dimensions. We believe it is useful to be able to convert, when possible, yupi trajectories to the data structures used by other libraries to\nempower our users with the tools offered by third parties. With the same spirit, we offer the possibility of converting data rom other libraries to yupi trajectories.\n\n## Installation\n\nCurrent recommended installation method is via the pypi package:\n\n```cmd\npip install yupiwrap\n```\n\nIt will install required dependencies such as [yupi package](https://pypi.org/project/yupi/) from pypi.\n\n## Compatible libraries\n\n### traja\n\nThe [Traja Python package](https://traja.readthedocs.io/en/latest/index.html) is a toolkit for the numerical characterization and analysis of the trajectories of moving animals. It provides several machine learning tools that are not yet implemented in yupi. Even when it is limited to two-dimensional trajectories, there are many resources that traja can offer when dealing with 2D Trajectories in [yupi](https://yupi.readthedocs.io/en/latest/).\n\n#### Converting a *yupi.Trajectory* into a *traja DataFrame*\n\nLet\'s create a trajectory with yupi:\n\n```python\nfrom yupi import Trajectory\n\nx = [0, 1.0, 0.63, -0.37, -1.24, -1.5, -1.08, -0.19, 0.82, 1.63, 1.99, 1.85]\ny = [0, 0, 0.98, 1.24, 0.69, -0.3, -1.23, -1.72, -1.63, -1.01, -0.06, 0.94]\n\ntrack = Trajectory(x=x, y=y, traj_id="Spiral")\n```\n\nWe can convert it to a traja DataFrame simply by:\n\n```python\nfrom yupiwrap import yupi2traja\n\ntraja_track = yupi2traja(track)\n```\n\n⚠️ Only *yupi.Trajectory* objects with two dimensions can be converted to *traja DataFrame* due to traja limitations.\n\n#### Converting a *traja DataFrame* into a *yupi.Trajectory*\n\nIf you have a *traja DataFrame* you can always convert it to a *yupi.Trajectory* by using:\n\n```python\nfrom yupiwrap import traja2yupi\n\nyupi_track = traja2yupi(traja_track)\n```\n',
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

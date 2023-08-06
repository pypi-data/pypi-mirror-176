# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trajan']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5',
 'netCDF4>=1.6',
 'numpy>=1.23',
 'pyproj>=2.3',
 'scipy>=1.9',
 'xarray>=2022.6.0']

setup_kwargs = {
    'name': 'trajan',
    'version': '0.1.0',
    'description': 'Trajectory analysis package for simulated and observed trajectories',
    'long_description': None,
    'author': 'Gaute Hope',
    'author_email': 'gauteh@met.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

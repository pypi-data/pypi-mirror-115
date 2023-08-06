# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neogidashboard',
 'neogidashboard.ensembles',
 'neogidashboard.ensembles.rashg',
 'neogidashboard.ensembles.stellarnet',
 'neogidashboard.visualizer',
 'neogidashboard.visualizer.rashg',
 'neogidashboard.visualizer.stellarnet']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.3.2,<3.0.0',
 'colorcet>=2.0.6,<3.0.0',
 'dask[distributed]>=2021.7.0,<2022.0.0',
 'hvplot>=0.7.2,<0.8.0',
 'matplotlib>=3.4.2,<4.0.0',
 'neogiinstruments>=2.6.0,<3.0.0',
 'netCDF4>=1.5.7,<2.0.0',
 'numba>=0.53.1,<0.54.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.2.5,<2.0.0',
 'panel>=0.11.3,<0.12.0',
 'plotly>=5.0.0,<6.0.0',
 'scipy>=1.7.0,<2.0.0',
 'simple-pid>=1.0.1,<2.0.0',
 'typing-extensions>=3.10.0,<4.0.0',
 'xarray>=0.18.2,<0.19.0',
 'zarr>=2.3,<3.0']

entry_points = \
{'console_scripts': ['clean = dashboard.console_utilities:clean',
                     'converter = neogidashboard.console_utilities:convert',
                     'dashboard = neogidashboard.combined:main']}

setup_kwargs = {
    'name': 'neogidashboard',
    'version': '0.1.0',
    'description': 'Dashboard for visualizing data',
    'long_description': None,
    'author': 'bageljr',
    'author_email': 'aryanagarwal897@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.6,<3.10.0',
}


setup(**setup_kwargs)

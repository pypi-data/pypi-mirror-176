# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['saenopy', 'saenopy.gui']

package_data = \
{'': ['*'], 'saenopy': ['img/*']}

install_requires = \
['imagecodecs>=2022.9.26,<2023.0.0',
 'jointforces>=1.0.1,<2.0.0',
 'natsort>=8.2.0,<9.0.0',
 'numba>=0.56.4,<0.57.0',
 'numpy>=1.23.4,<2.0.0',
 'openpiv>=0.24.2,<0.25.0',
 'pyqt5>=5.15.7,<6.0.0',
 'pyvista>=0.37.0,<0.38.0',
 'pyvistaqt>=0.9.0,<0.10.0',
 'qimage2ndarray>=1.9.0,<2.0.0',
 'qtawesome>=1.2.1,<2.0.0',
 'scipy>=1.9.3,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

extras_require = \
{'docs': ['sphinx-rtd-theme>=1.1.1,<2.0.0', 'nbsphinx>=0.8.10,<0.9.0']}

entry_points = \
{'console_scripts': ['saenopy = saenopy.gui_master:main']}

setup_kwargs = {
    'name': 'saenopy',
    'version': '0.8.0',
    'description': 'Semi-elastic fiber optimisation in python.',
    'long_description': 'SAENOPY\n=======\n\n[![DOC](https://readthedocs.org/projects/saenopy/badge/)](https://saenopy.readthedocs.io)\n[![PyTest](https://github.com/rgerum/saenopy/actions/workflows/test.yml/badge.svg)](https://github.com/rgerum/saenopy/actions/workflows/test.yml)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n<p align="center">\n  <img src="saenopy/img/Logo.png" />\n</p>\n\n\n\nSAENOPY a python implementation of the SAENO - Semi-affine Elastic Network Optimizer, originally developed by Julian\n Steinwachs.\n\n[Documentation](https://saenopy.readthedocs.io)\n',
    'author': 'rgerum',
    'author_email': '14153051+rgerum@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

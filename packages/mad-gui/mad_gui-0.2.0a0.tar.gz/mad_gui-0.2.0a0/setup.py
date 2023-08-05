# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mad_gui',
 'mad_gui.components',
 'mad_gui.components.dialogs',
 'mad_gui.config',
 'mad_gui.models',
 'mad_gui.plot_tools',
 'mad_gui.plugins',
 'mad_gui.qt_designer',
 'mad_gui.utils',
 'mad_gui.windows']

package_data = \
{'': ['*'], 'mad_gui.qt_designer': ['images/*']}

install_requires = \
['PySide2==5.15.1',
 'numpy>=1.19.2,<2.0.0',
 'openpyxl>=3.0.6,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pyqtgraph==0.11.0',
 'pytest>=6.2.2,<7.0.0',
 'scipy>=1.5.2,<2.0.0',
 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'mad-gui',
    'version': '0.2.0a0',
    'description': 'GUI for annotating and processing IMU data.',
    'long_description': None,
    'author': 'Malte Ollenschlaeger',
    'author_email': 'malte.ollenschlaeger@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)

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
    'version': '0.2.0a2',
    'description': 'GUI for annotating and processing IMU data.',
    'long_description': '# MaD GUI \n**M**achine Learning \n**a**nd \n**D**ata Analytics \n**G**raphical \n**U**ser \n**I**nterface\n\n![Test and Lint](https://github.com/mad-lab-fau/mad-gui/workflows/Test%20and%20Lint/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/mad-gui/badge/?version=latest)](https://mad-gui.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n##  What is it?\nThe MaD GUI is a framework for processing time series data.\nIts use-cases include visualization, annotation (manual or automated), and algorithmic processing of visualized data and annotations.\n\n## How do I use it?\n<soon there will be one or more videos here, which show(s) how the GUI works>\n\n- loading data / video / annotations\n- adding annotations via an algorithm\n- synchronize video and data\n- export data / apply other algorithms and export results\n\n## How do I get the GUI to work on my machine?\nBelow, we present two options how to obtain and run the GUI.\nHowever, this will only enable you to look at our example data.\nYou want to load data of a specific format/system or want to use a specific algorithm? \nIn this case please refer to ["Can I use it with data of my specific system or a specific algorithm?"](#can-i-use-it-with-data-of-my-specific-system-or-a-specific-algorithm).\n\n## How can I test the GUI using your example data on my computer?\n\nFirst, you need to download the example data.\nRight click on [this link](https://raw.githubusercontent.com/mad-lab-fau/mad-gui/main/example_data/smartphone/acceleration.csv), select `Save link as...` and save it as `acceleration.csv`.\nIf you also want to check out synchronization with a video file, then right click on [this link](https://github.com/mad-lab-fau/mad-gui/raw/main/example_data/smartphone/video/video.mp4) and select `Save link as...` to store it on your machine.\n\n### Option A: Standalone executable\n\n- Windows users: download our exemplary executable [here](https://github.com/mad-lab-fau/mad-gui/releases/download/v0.2.0-alpha.1/mad_gui.exe)\n- Other operating systems: [Contact us](mailto:mad-digait@fau.de).\n\nStart the program and then you can open the previously downloaded example data as shown in [How do I use it?](#how-do-i-use-it).\n\n### Option B: Using the python package\n```\npip install mad_gui\n```\nMake sure to include the underscore.\nIf you do not include it, you will install a different package.\n\nThen, from your command line either simply start the GUI or pass additional arguments:\n```\npython -m mad_gui.start_gui\npython -m mad_gui.starg_gui --base_dir C:/my_data\n```\n\nAlternatively, within a python script use our [start_gui](https://github.com/mad-lab-fau/mad-gui/blob/2857ccc20766ea32f847271771b52c97e2682b79/mad_gui/start_gui.py#L26) \nfunction and hand it over the path where your data resides, `<data_path>` like `"C:/data"` or `"/home/data/"`: \n```\nfrom mad_gui import start_gui\nstart_gui(<data_path>)\n```\n\nNow you can open the previously downloaded example data as shown in [How do I use it?](#how-do-i-use-it).\n\n\n## Can I use it with data of my specific system or a specific algorithm?\nYes, however it will need someone who is familiar with python.\nYou do not have experience with python but still want to load data from a specific system? [Contact us!](mailto:malte.ollenschlaeger@fau.de)\n\nDevelopers can get basic information about the project setup in our [Developer Guidelines](https://mad-gui.readthedocs.io/en/latest/developer_guidelines.html).\nIf you want extend the GUI with your custom plugins, e.g. for loading data of a specific system,\nor adding an algorithm, the necessary information can be found in our [API Reference](https://mad-gui.readthedocs.io/en/latest/api_reference.html).\n\n## Can I change something at the core of the GUI?\nSure, we try to document the most important parts of the GUI to make adaption as easy as possible.\nFor more information, please take a look at our [Contribution Guidelines](https://mad-gui.readthedocs.io/en/latest/contribution_guidelines.html#contribution-guidelines).\n',
    'author': 'Malte Ollenschlaeger',
    'author_email': 'malte.ollenschlaeger@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mad-lab-fau/mad-gui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)

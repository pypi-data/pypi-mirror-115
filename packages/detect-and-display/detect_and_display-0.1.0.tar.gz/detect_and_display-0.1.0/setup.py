# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['detect_and_display',
 'detect_and_display.utils',
 'detect_and_display_cli',
 'detect_and_display_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['detect_and_display = '
                     'detect_and_display_cli.detect_and_display_cli:cli']}

setup_kwargs = {
    'name': 'detect-and-display',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'patricio tula',
    'author_email': 'tula.patricio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tykes', 'tykes.farkle', 'tykes.flood']

package_data = \
{'': ['*']}

install_requires = \
['arcade>=2.6.16,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pygame>=2.1.2,<3.0.0',
 'typer>=0.6.1,<0.7.0']

setup_kwargs = {
    'name': 'tykes',
    'version': '1.0.0',
    'description': 'A python project designed to provide low-stimulation games to young children.',
    'long_description': '# Tikes\n\nThis python package is designed to distribute a few simple, low stimulation games for kids.\n\nThe intent is to introduce kids to games and interactive media in a safe, controllable\nenvironment.\n\nI love you, son.\n\n',
    'author': 'Ian Wernecke',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

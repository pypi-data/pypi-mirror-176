# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chesspos',
 'chesspos.evaluation',
 'chesspos.models',
 'chesspos.preprocessing',
 'chesspos.search',
 'chesspos.test',
 'chesspos.tools',
 'chesspos.utils']

package_data = \
{'': ['*']}

install_requires = \
['chess>=1.9.3,<2.0.0',
 'colorama>=0.4.6,<0.5.0',
 'h5py>=3.7.0,<4.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.23.4,<2.0.0',
 'tensorflow>=2.10.0,<3.0.0']

setup_kwargs = {
    'name': 'chess-embedding',
    'version': '0.1.4',
    'description': 'A library for manipulating, learning and searching on chess positions.',
    'long_description': None,
    'author': 'Patrick Frank',
    'author_email': 'patr.frank@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

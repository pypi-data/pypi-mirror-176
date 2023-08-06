# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bioacme']

package_data = \
{'': ['*'], 'bioacme': ['bin/*']}

entry_points = \
{'console_scripts': ['build_state_space_bfs = '
                     'bioacme.__main__:build_state_space_bfs',
                     'build_state_space_dfs = '
                     'bioacme.__main__:build_state_space_dfs',
                     'mxexp = bioacme.__main__:mxexp',
                     'net2matrix = bioacme.__main__:net_2_matrix',
                     'ssor = bioacme.__main__:ssor']}

setup_kwargs = {
    'name': 'bioacme',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Ali Farhat',
    'author_email': 'afarha5@uic.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitsrun']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['bitsrun = bitsrun.cli:main']}

setup_kwargs = {
    'name': 'bitsrun',
    'version': '3.1.0',
    'description': 'A headless login / logout script for 10.0.0.55',
    'long_description': 'None',
    'author': 'spencerwooo',
    'author_email': 'spencer.woo@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)

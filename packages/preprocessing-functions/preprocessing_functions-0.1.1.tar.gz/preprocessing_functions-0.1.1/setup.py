# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['preprocessing_functions']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0', 'numpy>=1.19,<2.0']

setup_kwargs = {
    'name': 'preprocessing-functions',
    'version': '0.1.1',
    'description': 'Common preprocessing functions for image deep learning applications packaged independently in order to avoid installing hefty packages such as tensorflow or pytorch in production.',
    'long_description': None,
    'author': 'Panagiotis Galopoulos',
    'author_email': 'gl.panagiotis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exp4']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.1,<2.0.0', 'scipy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'exp4',
    'version': '0.1.0',
    'description': 'Implementation of Exponential weighting for Exploration and Exploitation with Experts.',
    'long_description': '# exp4',
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)

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
    'version': '0.1.1',
    'description': 'Implementation of Exponential weighting for Exploration and Exploitation with Experts.',
    'long_description': "# EXP4 \nA python implementation of Exponential weighting for Exploration and Exploitation with Experts. Based on [this blog post](https://banditalgs.com/2016/10/14/exp4/).\n\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/exp4/status.svg)](https://cloud.drone.io/mvcisback/exp4)\n[![PyPI version](https://badge.fury.io/py/exp4.svg)](https://badge.fury.io/py/exp4)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n**Table of Contents**\n\n- [Installation](#installation)\n- [Usage](#usage)\n\n# Installation\n\nIf you just need to use `exp4`, you can just run:\n\n`$ pip install exp4`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then\nrun:\n\n`$ poetry install`\n\n# Usage\n\n`exp4` is centered around the `exp4.exp4` function which creates a\nco-routine for selecting arms given expert advice.\n\nThe protocol is as follows:\n\n1. The expert constructs an expert advice matrix.\n   - Each row contains the corresponding experts advice vector.\n   - The advice vector provides probabilities for each arm.\n2. The expert sends a tuple of loss and advice.\n   - The loss corresponds to the previous round.\n   - The first round's loss is ignored.\n   - The advice correspond to the current round.\n\nAn example is given below.\n\n```python\nplayer = exp4()\n\nloss = None           # Will be ignored.\nadvice = [\n    [1/3, 1/3, 1/3],  # Expert 1 \n    [2/3, 1/3, 0],    # Expert 2\n]\narm = player.send((loss, advice))\nassert arm in range(3)\n\nloss = 1 / (1 + arm)  # Arbitrary loss assigned to arm.\nadvice = [\n    [0, 0, 1],        # Expert 1\n    [0, 0, 1],        # Expert 2\n]\narm = player.send((loss, advice))\nassert arm == 2\n```\n",
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

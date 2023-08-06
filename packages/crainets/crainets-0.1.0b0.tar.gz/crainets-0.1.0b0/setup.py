# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crainets',
 'crainets.base',
 'crainets.config',
 'crainets.essentials',
 'crainets.losses',
 'crainets.models',
 'crainets.models.ResXUNet',
 'crainets.models.UNet',
 'crainets.models.blocks',
 'crainets.models.blocks.BiFPN',
 'crainets.models.blocks.utils',
 'crainets.models.efficientnet',
 'crainets.trainer']

package_data = \
{'': ['*']}

install_requires = \
['colorlog>=5.0.1,<6.0.0',
 'flake8>=3.9.2,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'py3nvml>=0.2.6,<0.3.0',
 'pytest>=6.2.4,<7.0.0',
 'torch>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'crainets',
    'version': '0.1.0b0',
    'description': 'deep learning utility library',
    'long_description': None,
    'author': 'JonNesvold',
    'author_email': 'jon.nesvold@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

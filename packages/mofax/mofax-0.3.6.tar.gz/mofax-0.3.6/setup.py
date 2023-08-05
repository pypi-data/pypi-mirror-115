# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mofax']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=2.9.0',
 'matplotlib>=3.1.0',
 'numpy>=1.17.0',
 'pandas>=1.0.0',
 'seaborn>=0.9.0']

setup_kwargs = {
    'name': 'mofax',
    'version': '0.3.6',
    'description': 'Work with MOFA+ models in Python',
    'long_description': None,
    'author': 'Danila Bredikhin',
    'author_email': 'danila.bredikhin@embl.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)

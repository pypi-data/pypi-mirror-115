# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['model_compression']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.1,<2.0.0', 'pytorch>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'model-compression-777',
    'version': '0.1.0',
    'description': 'Pre-pruned pytorch model compression toolkit',
    'long_description': None,
    'author': 'Richard Yan',
    'author_email': 'yrh@berkeley.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

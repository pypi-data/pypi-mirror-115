# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycatan', 'pycatan.board']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.7b0,<22.0',
 'colored>=1.4.2,<2.0.0',
 'flake8>=3.9.2,<4.0.0',
 'pytest-snapshot>=0.6.1,<0.7.0',
 'sphinx-autodoc-typehints>=1.12.0,<2.0.0',
 'sphinx-rtd-theme>=0.5.2,<0.6.0']

setup_kwargs = {
    'name': 'pycatan',
    'version': '0.2.0',
    'description': 'A library for running games of The Settlers of Catan',
    'long_description': None,
    'author': 'Josef Waller',
    'author_email': 'josef@siriusapplications.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

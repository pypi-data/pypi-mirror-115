# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycatan', 'pycatan.board']

package_data = \
{'': ['*']}

install_requires = \
['colored>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'pycatan',
    'version': '1.0.1',
    'description': 'A library for running games of The Settlers of Catan',
    'long_description': None,
    'author': 'Josef Waller',
    'author_email': 'josef@siriusapplications.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/josefwaller/PyCatan2',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

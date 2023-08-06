# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beavis']

package_data = \
{'': ['*']}

install_requires = \
['dask>2021.01.1', 'pandas>=1.0.0']

setup_kwargs = {
    'name': 'beavis',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'MrPowers',
    'author_email': 'matthewkevinpowers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynomics']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2',
 'nomics-python>=3.2.0,<4.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.1,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'tqdm>=4.62.0,<5.0.0']

setup_kwargs = {
    'name': 'pynomics',
    'version': '0.1.1',
    'description': 'Small library to interact with the [Nomics api](https://p.nomics.com/cryptocurrency-bitcoin-api).',
    'long_description': None,
    'author': 'Soumendra Prasad Dhanee',
    'author_email': 'soumendra@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)

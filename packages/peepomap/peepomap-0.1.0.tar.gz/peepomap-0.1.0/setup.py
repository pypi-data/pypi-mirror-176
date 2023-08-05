# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peepomap']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.0,<4.0.0', 'numpy>=1.21.4,<2.0.0']

setup_kwargs = {
    'name': 'peepomap',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'ericmiguel',
    'author_email': 'ericmiguel@id.uff.br',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.11',
}


setup(**setup_kwargs)

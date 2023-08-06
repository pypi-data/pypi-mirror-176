# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tabular_data']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1.0,<23.0.0']

setup_kwargs = {
    'name': 'tabular-data',
    'version': '0.1.0',
    'description': 'The sensible way to work with tabular data',
    'long_description': '# tabular-data\n\nThe sensible way to work with tabular data\n\n',
    'author': 'Juan Gonzalez',
    'author_email': 'jrg2156@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

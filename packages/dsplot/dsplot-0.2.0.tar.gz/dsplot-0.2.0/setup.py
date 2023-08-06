# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dsplot', 'dsplot.graph', 'dsplot.tree']

package_data = \
{'': ['*']}

install_requires = \
['pygraphviz>=1.7,<2.0']

setup_kwargs = {
    'name': 'dsplot',
    'version': '0.2.0',
    'description': 'Plot data structures with ease.',
    'long_description': '',
    'author': 'Bill',
    'author_email': 'trantriducs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

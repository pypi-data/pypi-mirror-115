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
    'version': '0.3.0',
    'description': 'Plot data structures with ease.',
    'long_description': '# Data Structure Plot (DSPlot)\n[![Build Status](https://travis-ci.com/billtrn/dsplot.svg?branch=master)](https://travis-ci.com/billtrn/dsplot)\n[![Coverage Status](https://coveralls.io/repos/github/billtrn/dsplot/badge.svg?branch=master)](https://coveralls.io/github/billtrn/dsplot?branch=master)\n[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/billtrn/dsplot/blob/master/LICENSE)\n\n## 📄 License\n[MIT](./LICENSE)\n',
    'author': 'Bill',
    'author_email': 'trantriducs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

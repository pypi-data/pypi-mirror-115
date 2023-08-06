# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plotnine_prism']

package_data = \
{'': ['*'], 'plotnine_prism': ['schemes/*']}

install_requires = \
['diot>=0.1.1,<0.2.0', 'plotnine>=0.8.0,<0.9.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'plotnine-prism',
    'version': '0.0.0',
    'description': 'Prism themes for plotnine, inspired by ggprism',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

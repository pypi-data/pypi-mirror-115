# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recmetrics_new']

package_data = \
{'': ['*']}

install_requires = \
['funcsigs>=1.0.2,<2.0.0',
 'matplotlib>=3.3.2,<4.0.0',
 'pandas>=1.1.5,<2.0.0',
 'plotly>=4.11.0,<5.0.0',
 'pytest-cov>=2.10.1,<3.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'scikit-surprise>=1.1.1,<2.0.0',
 'scipy>=1.5.2,<2.0.0',
 'seaborn>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'recmetrics-new',
    'version': '0.3.1',
    'description': 'A library of metrics for evaluating recommender systems',
    'long_description': None,
    'author': 'Daniil Smirnov',
    'author_email': 'den762000@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlconfound']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mlconfound',
    'version': '0.9.0',
    'description': 'Tools for analyzing and quantifying effects of counfounder variables on machine learning model predictions.',
    'long_description': None,
    'author': 'Tamas Spisak',
    'author_email': 'tamas.spisak@uk-essen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

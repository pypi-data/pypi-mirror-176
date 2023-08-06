# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['decorworld_database_model']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy==1.3.18']

setup_kwargs = {
    'name': 'decorworld-database-model',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Pintér Tamás',
    'author_email': 'tamas.pinter@pannonszoftver.hu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

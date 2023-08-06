# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['immuna_prices']

package_data = \
{'': ['*']}

install_requires = \
['cryptocmd>=0.6.1,<0.7.0',
 'load-dotenv>=0.1.0,<0.2.0',
 'pandas>=1.5.1,<2.0.0',
 'peewee>=3.15.3,<4.0.0',
 'prisma>=0.7.0,<0.8.0',
 'psycopg2-binary>=2.9.5,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'i-prices',
    'version': '1.0.0',
    'description': '',
    'long_description': '# Prices stuff\n',
    'author': 'Dima v',
    'author_email': 'dima@immuna.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

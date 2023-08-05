# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataasset', 'dataasset.alembic', 'dataasset.alembic.versions']

package_data = \
{'': ['*']}

extras_require = \
{'mssql': ['SQLAlchemy>=1.4,<2.0',
           'sqlalchemy-json>=0.5,<0.6',
           'alembic>=1.8,<2.0',
           'pyodbc>=4.0.34,<5.0.0'],
 'mysql': ['SQLAlchemy>=1.4,<2.0',
           'sqlalchemy-json>=0.5,<0.6',
           'alembic>=1.8,<2.0',
           'pymysql>=1.0,<2.0'],
 'postgres': ['psycopg2>=2.9,<3.0',
              'SQLAlchemy>=1.4,<2.0',
              'sqlalchemy-json>=0.5,<0.6',
              'alembic>=1.8,<2.0']}

entry_points = \
{'console_scripts': ['dataasset = dataasset.application:main']}

setup_kwargs = {
    'name': 'dataasset',
    'version': '0.4.3',
    'description': '',
    'long_description': 'None',
    'author': 'c-jamie',
    'author_email': 'jamie.b.clery@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

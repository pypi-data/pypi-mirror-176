# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databudgie', 'databudgie.adapter', 'databudgie.cli', 'databudgie.manifest']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0.0',
 'configly[yaml]',
 'rich',
 'sqlalchemy>=1.3',
 'strapp[click,sqlalchemy]>=0.2.7']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.10.0', 'importlib-metadata'],
 'psycopg2': ['psycopg2>=2.7'],
 'psycopg2-binary': ['psycopg2-binary>=2.7'],
 's3': ['boto3'],
 'sentry': ['sentry-sdk']}

entry_points = \
{'console_scripts': ['databudgie = databudgie.__main__:run']}

setup_kwargs = {
    'name': 'databudgie',
    'version': '2.7.0',
    'description': '',
    'long_description': 'None',
    'author': 'Andrew Sosa',
    'author_email': 'andrewso@known.is',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)

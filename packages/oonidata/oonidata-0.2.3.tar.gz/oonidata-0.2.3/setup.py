# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oonidata', 'oonidata.cli', 'oonidata.db', 'oonidata.experiments']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0',
 'boto3>=1.24',
 'click>=8.0.0',
 'clickhouse-driver>=0.2',
 'cryptography>=38.0.3',
 'lxml>=4.9',
 'lz4>=4.0',
 'mashumaro>=3.0',
 'maxminddb>=2.2',
 'orjson>=3.8',
 'pyOpenSSL>=22.1',
 'requests>=2.27',
 'tqdm>=4.64']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0']}

entry_points = \
{'console_scripts': ['oonidata = oonidata.cli:cli']}

setup_kwargs = {
    'name': 'oonidata',
    'version': '0.2.3',
    'description': '',
    'long_description': None,
    'author': 'Arturo Filastò',
    'author_email': 'arturo@filasto.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)

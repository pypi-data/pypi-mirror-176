# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['watchmen_data_surface',
 'watchmen_data_surface.cache',
 'watchmen_data_surface.data']

package_data = \
{'': ['*']}

install_requires = \
['watchmen-data-kernel==16.4.3', 'watchmen-rest==16.4.3']

extras_require = \
{'mongodb': ['watchmen-storage-mongodb==16.4.3'],
 'mssql': ['watchmen-storage-mssql==16.4.3'],
 'mysql': ['watchmen-storage-mysql==16.4.3'],
 'oracle': ['watchmen-storage-oracle==16.4.3'],
 'oss': ['watchmen-storage-oss==16.4.3'],
 'postgresql': ['watchmen-storage-postgresql==16.4.3'],
 's3': ['watchmen-storage-s3==16.4.3']}

setup_kwargs = {
    'name': 'watchmen-data-surface',
    'version': '16.4.3',
    'description': '',
    'long_description': 'None',
    'author': 'botlikes',
    'author_email': '75356972+botlikes456@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

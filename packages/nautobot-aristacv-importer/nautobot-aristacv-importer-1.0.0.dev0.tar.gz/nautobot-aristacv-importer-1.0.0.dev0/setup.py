# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_aristacv_importer', 'nautobot_aristacv_importer.diffsync']

package_data = \
{'': ['*']}

install_requires = \
['cloudvision>=1.0.0,<2.0.0',
 'diffsync>=1.3.0,<2.0.0',
 'pydantic[dotenv]>=1.7.2,<2.0.0',
 'pynautobot>=1.0.2,<2.0.0',
 'toml==0.10.1']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['nautobot_aristacv_importer = '
                     'nautobot_aristacv_importer.cli:main']}

setup_kwargs = {
    'name': 'nautobot-aristacv-importer',
    'version': '1.0.0.dev0',
    'description': 'Import CloudVision tags to Nautobot',
    'long_description': None,
    'author': 'Network to Code, LLC',
    'author_email': 'info@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

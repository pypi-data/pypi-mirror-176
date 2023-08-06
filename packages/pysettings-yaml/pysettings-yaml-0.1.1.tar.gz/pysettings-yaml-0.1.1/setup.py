# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysettings_yaml', 'pysettings_yaml.providers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'deepmerge>=1.1.0,<2.0.0',
 'funcy>=1.17,<2.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-decouple>=3.6,<4.0',
 'split-settings>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'pysettings-yaml',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'David',
    'author_email': 'davigetto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

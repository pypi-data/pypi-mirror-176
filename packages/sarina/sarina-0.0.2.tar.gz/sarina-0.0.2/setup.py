# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sarina',
 'sarina.cli',
 'sarina.core',
 'sarina.monitoring',
 'sarina.providers',
 'sarina.templates']

package_data = \
{'': ['*']}

install_requires = \
['deepdiff>=6.2.1,<7.0.0',
 'inquirerpy>=0.3.4,<0.4.0',
 'paramiko>=2.12.0,<3.0.0',
 'python-digitalocean>=1.17.0,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'rich>=12.6.0,<13.0.0',
 'tld>=0.12.6,<0.13.0',
 'tqdm>=4.60.0,<5.0.0']

entry_points = \
{'console_scripts': ['sarina = sarina:main']}

setup_kwargs = {
    'name': 'sarina',
    'version': '0.0.2',
    'description': '',
    'long_description': 'None',
    'author': 'Hadi',
    'author_email': 'hadi.zolfaghaari@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pacmine',
 'pacmine.core',
 'pacmine.local',
 'pacmine.local.discovery',
 'pacmine.local.serialize',
 'pacmine.remote']

package_data = \
{'': ['*']}

install_requires = \
['Columnar>=1.3.1,<2.0.0',
 'arrow>=1.1.1,<2.0.0',
 'fire>=0.4.0,<0.5.0',
 'requests>=2.26.0,<3.0.0',
 'semantic-version>=2.8.5,<3.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'tqdm>=4.62.0,<5.0.0']

entry_points = \
{'console_scripts': ['pacmine = pacmine.__main__:main']}

setup_kwargs = {
    'name': 'pacmine',
    'version': '1.0.2',
    'description': '',
    'long_description': None,
    'author': 'aidan',
    'author_email': 'aidan.chaplin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

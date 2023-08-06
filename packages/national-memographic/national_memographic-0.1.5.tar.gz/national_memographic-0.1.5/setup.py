# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['national_memographic',
 'national_memographic._bot',
 'national_memographic._cli',
 'national_memographic._cli.native',
 'national_memographic._cli.twitter',
 'national_memographic._twitter']

package_data = \
{'': ['*']}

install_requires = \
['Wand>=0.6.6,<0.7.0',
 'click>=8.0.1,<9.0.0',
 'requests>=2.26.0,<3.0.0',
 'requests_oauthlib>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['meme = national_memographic.__main__:main']}

setup_kwargs = {
    'name': 'national-memographic',
    'version': '0.1.5',
    'description': 'The one and only Twitter meme bot',
    'long_description': None,
    'author': 'hacksparr0w',
    'author_email': 'hacksparr0w@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

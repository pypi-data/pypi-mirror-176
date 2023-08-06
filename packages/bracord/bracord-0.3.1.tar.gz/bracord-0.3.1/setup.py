# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bracord', 'bracord.cli']

package_data = \
{'': ['*']}

install_requires = \
['disnake>=2.7.0,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'rich>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['bracord = disnake.ext.bracord.entry:main']}

setup_kwargs = {
    'name': 'bracord',
    'version': '0.3.1',
    'description': 'A Disnake framework written in Python that speeds the development of Discord bots.',
    'long_description': '# Bracord\nA [Disnake](https://github.com/DisnakeDev/Disnake) framework written in Python that speeds the development of Discord bots.',
    'author': 'MrFellox',
    'author_email': 'jfernandohernandez28@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mrfellox/bracord',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

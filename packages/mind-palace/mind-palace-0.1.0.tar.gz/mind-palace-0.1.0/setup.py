# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mind_palace']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['mind-palace = mind_palace:main']}

setup_kwargs = {
    'name': 'mind-palace',
    'version': '0.1.0',
    'description': 'Note management application',
    'long_description': '',
    'author': 'Jerven Clark Chua',
    'author_email': 'jervenclark@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jervenclark/mind-palace',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

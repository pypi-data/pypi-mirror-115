# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['firstappqjy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['wow = entry:main']}

setup_kwargs = {
    'name': 'firstappqjy',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'SoftJing1',
    'author_email': '118010248@link.cuhk.edu.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

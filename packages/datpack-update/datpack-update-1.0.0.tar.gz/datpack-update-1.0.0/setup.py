# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datpack_update']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['datpack-update = datpack_update.datpack_update:main']}

setup_kwargs = {
    'name': 'datpack-update',
    'version': '1.0.0',
    'description': 'Update No-Intro DAT files',
    'long_description': None,
    'author': 'Andrew Simmons',
    'author_email': 'agsimmons0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

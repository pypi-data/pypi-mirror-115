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
    'version': '1.0.2',
    'description': 'Update No-Intro DAT files',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/datpack-update)](https://pypi.org/project/datpack-update/)\n\n# datpack-update\nUpdate No-Intro DAT files\n\n## Description\nThis script updates your current No-Intro dat files with new versions that you download. The benefit over doing this manually is that this program automatically finds which dat files you have in your existing folder, and only updates those dat files. This is helpful if you download the Daily datfile pack from [DAT-o-MATIC](https://datomatic.no-intro.org/).\n\nYour dat files **must** be named exactly as DAT-o-MATIC names them. This program relies on the specific timestamp format being used. Some examples names are:\n\n```\nAtari - 2600 (20200514-091155).dat\nBandai - WonderSwan (20210609-224257).dat\nSega - Master System - Mark III (20210527-151920).dat\n```\n\n## Usage\n```\nusage: datpack-update.py [-h] src dest\n\nUpdate No-Intro DAT files\n\npositional arguments:\n  src         Source directory of new DAT files\n  dest        Destination directory of updated DAT files\n\noptional arguments:\n  -h, --help  show this help message and exit\n```\n',
    'author': 'Andrew Simmons',
    'author_email': 'agsimmons0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agsimmons/datpack-update',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

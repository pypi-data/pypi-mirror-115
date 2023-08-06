# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kaggle_downloader']

package_data = \
{'': ['*']}

install_requires = \
['jupyter>=1.0.0,<2.0.0',
 'kaggle>=1.5.12,<2.0.0',
 'nbconvert>=6.1.0,<7.0.0',
 'nbformat>=5.1.3,<6.0.0']

entry_points = \
{'console_scripts': ['kaggle-downloader = kaggle_downloader.main:main']}

setup_kwargs = {
    'name': 'kaggle-downloader',
    'version': '1.0.0',
    'description': 'Download kernels from Kaggle.',
    'long_description': None,
    'author': 'Lars Reimann',
    'author_email': 'mail@larsreimann.com',
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

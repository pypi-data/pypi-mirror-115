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
    'version': '1.0.2',
    'description': 'Download kernels from Kaggle.',
    'long_description': '# kaggle-downloader\n\nA wrapper around the Kaggle CLI to download multiple kernels at once.\n\n## Installation\n\n1. Grab the latest release of [Python](https://www.python.org/downloads/release).\n2. Install this tool with `pip install kaggle-downloader`.\n3. Follow the steps from the [Kaggle API documentation](https://github.com/Kaggle/kaggle-api#api-credentials) to create an API token. We never access this directly but let the official Kaggle API take care of authentication.\n\n## Usage\n\n```text\nusage: kaggle-downloader [-h] {competition-refs,kernel-refs,kernels} ...\n\nDownload kernels from Kaggle.\n\npositional arguments:\n  {competition-refs,kernel-refs,kernels}\n    competition-refs    Fetch competition references.\n    kernel-refs         Fetch kernel references for a list of competition references.\n    kernels             Fetch kernels for a list of kernel references.\n\noptional arguments:\n  -h, --help            show this help message and exit\n```\n\nGetting to the actual kernels takes three steps:\n1. Get a list of references to competitions:\n    ```text\n    usage: kaggle-downloader competition-refs [-h] -o OUT\n\n    optional arguments:\n      -h, --help         show this help message and exit\n      -o OUT, --out OUT  Output file.\n    ```\n2. Get a list of references to kernels:\n    ```text\n    usage: kaggle-downloader kernel-refs [-h] -c COMPETITIONS -e EXCLUDE -o OUT\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      -c COMPETITIONS, --competitions COMPETITIONS\n                            File with list of competitions references.\n      -e EXCLUDE, --exclude EXCLUDE\n                            File with list of competitions references to exclude. Gets updated with competitions as they are processed.\n      -o OUT, --out OUT     Output directory.\n    ```\n3. Get kernels themselves:\n    ```text\n    usage: kaggle-downloader kernels [-h] -k KERNELS -e EXCLUDE -o OUT\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      -k KERNELS, --kernels KERNELS\n                            Directory with files containing a list of kernel references.\n      -e EXCLUDE, --exclude EXCLUDE\n                            File with list of kernel references to exclude. Gets updated with kernels as they are processed.\n      -o OUT, --out OUT     Output directory.\n\n    ```\n\n\n### Example usage\n\n```bash\n# Step 1:\nkaggle-downloader competition-refs -o data/competition-refs.txt\n\n# Step 2:\nkaggle-downloader kernel-refs -c data/competition-refs.txt -e data/excluded-competition-refs.txt -o data/kernel-refs\n\n# Step 3:\nkaggle-downloader kernels -k data/kernel-refs -e data/excluded-kernel-refs.txt -o data/kernels\n```\n\n## For developers\n\n1. Grab the latest release of [Python](https://www.python.org/downloads/release).\n2. Install [poetry](https://python-poetry.org/).\n3. Run `poetry install` in the root of the repository.\n4. Set the Python interpreter in your IDE to the virtual environment that was created.\n',
    'author': 'Lars Reimann',
    'author_email': 'mail@larsreimann.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lars-reimann/kaggle-downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

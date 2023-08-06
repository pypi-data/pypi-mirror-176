# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['embodyfile']

package_data = \
{'': ['*']}

install_requires = \
['embody-codec>1.0.9', 'matplotlib>=3.6.2', 'pandas>=1.5.1']

entry_points = \
{'console_scripts': ['embody-file = embodyfile.cli:main']}

setup_kwargs = {
    'name': 'embody-file',
    'version': '1.0.1',
    'description': 'Embody file converter',
    'long_description': '# Embody File\n\n[![PyPI](https://img.shields.io/pypi/v/embody-file.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/embody-file.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/embody-file)][python version]\n[![License](https://img.shields.io/pypi/l/embody-file)][license]\n\n[![Tests](https://github.com/aidee-health/embody-file/workflows/Tests/badge.svg)][tests]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/embody-file/\n[status]: https://pypi.org/project/embody-file/\n[python version]: https://pypi.org/project/embody-file\n[tests]: https://github.com/aidee-health/embody-file/actions?workflow=Tests\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nThis is a Python based implementation for parsing binary files from the Aidee EmBody device.\n\n## Features\n\n- Converts binary embody files to HDF, CSV, etc\n- Integrates with [the EmBody Protocol Codec](https://github.com/aidee-health/embody-protocol-codec) project\n- CLI (command line interface)\n- Can be used as package in other projects\n- Type safe code using [mypy](https://mypy.readthedocs.io/) for type checking\n\n## Requirements\n\n- Python 3.8-3.11\n\n## Installation\n\nYou can install _Embody File_ via [pip]:\n\n```console\n$ pip install embody-file\n```\n\n## Usage\n\nTo use the command line, first install this library either globally or using venv:\n\n```console\n$ pip install embody-file\n```\n\nWhen this library has been installed, a new command is available, `embody-file` which can be used according to the examples below:\n\n### Get help\n\nTo get an updated overview of all command line options:\n\n```bash\nembody-file --help\n```\n\n### Print version number\n\n```bash\nembody-file --version\n```\n\n### Convert binary embody file to HDF\n\nTo convert to a [HDF 5 (hierarcical data format)](https://en.wikipedia.org/wiki/Hierarchical_Data_Format) format, run the following:\n\n```bash\nembody-file testfiles/v5_0_0_test_file.log --output-format HDF\n```\n\nThe file will be named the same as the input file, with the `.hdf` extension at the end of the file name.\n\n### Convert binary embody file to CSV\n\nTo convert to CSV format, run the following:\n\n```bash\nembody-file testfiles/v5_0_0_test_file.log --output-format CSV\n```\n\nThe file will be named the same as the input file, with the `.csv` extension at the end of the file name.\n\n### Print statistics for binary embody file\n\nTo print stats without conversion:\n\n```bash\nembody-file testfiles/v5_0_0_test_file.log --print-stats\n```\n\n### Plot binary file in graph\n\nTo show an ECG/PPG plot graph:\n\n```bash\nembody-file testfiles/v5_0_0_test_file.log --plot\n```\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n[file an issue]: https://github.com/aidee-health/embody-file/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/aidee-health/embody-file/blob/main/LICENSE\n[contributor guide]: https://github.com/aidee-health/embody-file/blob/main/CONTRIBUTING.md\n[command-line reference]: https://embody-file.readthedocs.io/en/latest/usage.html\n',
    'author': 'Espen Westgaard',
    'author_email': 'espen@aidee.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aidee-health/embody-file',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)

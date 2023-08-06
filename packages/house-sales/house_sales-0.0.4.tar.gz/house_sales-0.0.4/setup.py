# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['house_sales',
 'house_sales.config',
 'house_sales.datasets',
 'house_sales.processing',
 'house_sales.trained_models']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1',
 'feature-engine>=1.5.1,<2.0.0',
 'joblib>=1.2.0,<2.0.0',
 'nox>=2022.8.7,<2023.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'pre-commit>=2.20.0,<3.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'scikit-learn>=1.1.3,<2.0.0',
 'scipy>=1.8.1,<2.0.0',
 'strictyaml>=1.6.2,<2.0.0']

entry_points = \
{'console_scripts': ['house-sales = house_sales.__main__:main']}

setup_kwargs = {
    'name': 'house-sales',
    'version': '0.0.4',
    'description': 'House Sales',
    'long_description': "# House Sales\n\n[![PyPI](https://img.shields.io/pypi/v/house-sales.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/house-sales.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/house-sales)][python version]\n[![License](https://img.shields.io/pypi/l/house-sales)][license]\n\n[![Read the documentation at https://house-sales.readthedocs.io/](https://img.shields.io/readthedocs/house-sales/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/paulrousset/house-sales/workflows/Tests/badge.svg)][tests]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/house-sales/\n[status]: https://pypi.org/project/house-sales/\n[python version]: https://pypi.org/project/house-sales\n[read the docs]: https://house-sales.readthedocs.io/\n[tests]: https://github.com/paulrousset/house-sales/actions?workflow=Tests\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _House Sales_ via [pip] from [PyPI]:\n\n```console\n$ pip install house-sales\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_House Sales_ is free and open source software.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/paulrousset/house-sales/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/paulrousset/house-sales/blob/main/LICENSE\n[command-line reference]: https://house-sales.readthedocs.io/en/latest/usage.html\n",
    'author': 'Paul Rousset',
    'author_email': 'paulrousset@hotmail.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/paulrousset/house-sales',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conda_hooks']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['conda_env_store = conda_hooks.env_store:main']}

setup_kwargs = {
    'name': 'conda-hooks',
    'version': '0.3.0',
    'description': 'Keep anaconda environment files up to date',
    'long_description': '# conda-hooks\n\nKeep anaconda environment files up to date with installed packages.\nThis can easily be automated using [pre-commit](https://pre-commit.com/) hooks.\n\n[![Build Status](https://img.shields.io/github/workflow/status/f-koehler/conda-hooks/build)](https://github.com/f-koehler/conda-hooks/actions)\n[![codecov](https://codecov.io/gh/f-koehler/conda-hooks/branch/main/graph/badge.svg?token=4XHPAHUDOL)](https://codecov.io/gh/f-koehler/conda-hooks)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/f-koehler/conda-hooks/main.svg)](https://results.pre-commit.ci/latest/github/f-koehler/conda-hooks/main)\n[![PyPI Version](https://img.shields.io/pypi/v/conda-hooks)](https://pypi.org/project/conda-hooks/)\n![License](https://img.shields.io/pypi/l/conda-hooks?color=blue)\n\n## Installation\n\n### As a python package\n\nThe `conda_hooks` package is installable as a normal python package, for example via pip:\n\n```bash\npip install conda_hooks\n```\n\n### As a `pre-commit` hook\n\nIn your `.pre-commit-config.yaml` file add\n\n```yaml\nrepos:\n  - repo: https://github.com/f-koehler/conda-hooks\n    rev: "0.2.2"\n    hooks:\n      - id: prettier\n```\n\n## Usage/Examples\n\nTODO\n',
    'author': 'Fabian Köhler',
    'author_email': 'fabian.koehler@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/f-koehler/conda-hooks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

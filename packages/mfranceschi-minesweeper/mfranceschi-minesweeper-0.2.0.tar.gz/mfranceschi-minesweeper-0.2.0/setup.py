# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mfranceschi_minesweeper',
 'mfranceschi_minesweeper.controller',
 'mfranceschi_minesweeper.model',
 'mfranceschi_minesweeper.view']

package_data = \
{'': ['*']}

install_requires = \
['overrides>=6.1,<7.0']

entry_points = \
{'console_scripts': ['mf-mines = mfranceschi_minesweeper.main:main']}

setup_kwargs = {
    'name': 'mfranceschi-minesweeper',
    'version': '0.2.0',
    'description': 'A cool minesweeper',
    'long_description': '# Mfranceschi Minesweeper\n\n[![My_CI](https://github.com/mfranceschi/Mfran-Minesweeper/actions/workflows/My_CI.yaml/badge.svg)](https://github.com/mfranceschi/Mfran-Minesweeper/actions/workflows/My_CI.yaml)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mfranceschi-minesweeper)\n[![PyPI license](https://img.shields.io/pypi/l/mfranceschi-minesweeper.svg)](https://pypi.python.org/pypi/mfranceschi-minesweeper/)\n\nSandbox repo for myself: write the best possible Minesweeper code!\n\n## Context\n\nI am doing this side-project as a hobby. It is relatively easy to write a working minesweeper but it\'s harder to code nicely. My intention here is to write and enhance my code as I learn new coding guidelines. I am currently learning from the following sources:\n\n- book "Clean Code" by Robert C. Martin (2002)\n- book "The Pragmatic Programmer" by Andy Hunt and Dave Thomas (2019 Remaster)\n- YouTuber ArjanCodes\n\n## How to use\n\nRequirements: Python >=3.7, Tkinter (for GUI code = for playing!). Helper for Debian: `sudo apt install -y python3.7 python3-tk`.\n\n### Using PyPI\n\nYou can download and install the package from PyPI:\n\n```sh\npip install mfranceschi-minesweeper\n```\n\n- Play the game by running directly in your terminal **`mf-mines`**.\n- Use the code by importing the package **`mfranceschi_minesweeper`** (beware of the underscore \'`_`\').\n\n### Git clone\n\nYou can also clone this repo! Once it is done:\n\n- Install dependencies with `pip install -r requirements.txt`.\n- Other packages used during development (not required to interpret the files): _pylint_, _pytest_, _mypy_.\n- Play the game by running from the repo\'s root `python .`\n  - It will actually execute the file `__main__.py`.\n- Use the code at will! Recommended IDE is VS Code since I used it and added a `.vscode/settings.json` file in the repo.\n',
    'author': 'mfranceschi',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mfranceschi/Minesweeper/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

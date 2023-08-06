# Mfranceschi Minesweeper

[![My_CI](https://github.com/mfranceschi/Mfran-Minesweeper/actions/workflows/My_CI.yaml/badge.svg)](https://github.com/mfranceschi/Mfran-Minesweeper/actions/workflows/My_CI.yaml)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mfranceschi-minesweeper)
[![PyPI license](https://img.shields.io/pypi/l/mfranceschi-minesweeper.svg)](https://pypi.python.org/pypi/mfranceschi-minesweeper/)

Sandbox repo for myself: write the best possible Minesweeper code!

## Context

I am doing this side-project as a hobby. It is relatively easy to write a working minesweeper but it's harder to code nicely. My intention here is to write and enhance my code as I learn new coding guidelines. I am currently learning from the following sources:

- book "Clean Code" by Robert C. Martin (2002)
- book "The Pragmatic Programmer" by Andy Hunt and Dave Thomas (2019 Remaster)
- YouTuber ArjanCodes

## How to use

Requirements: Python >=3.7, Tkinter (for GUI code = for playing!). Helper for Debian: `sudo apt install -y python3.7 python3-tk`.

### Using PyPI

You can download and install the package from PyPI:

```sh
pip install mfranceschi-minesweeper
```

- Play the game by running directly in your terminal **`mf-mines`**.
- Use the code by importing the package **`mfranceschi_minesweeper`** (beware of the underscore '`_`').

### Git clone

You can also clone this repo! Once it is done:

- Install dependencies with `pip install -r requirements.txt`.
- Other packages used during development (not required to interpret the files): _pylint_, _pytest_, _mypy_.
- Play the game by running from the repo's root `python .`
  - It will actually execute the file `__main__.py`.
- Use the code at will! Recommended IDE is VS Code since I used it and added a `.vscode/settings.json` file in the repo.

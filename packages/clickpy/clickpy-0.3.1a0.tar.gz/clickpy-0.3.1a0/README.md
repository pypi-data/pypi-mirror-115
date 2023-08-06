# clickpy

Automated mouse clicker script.

## Dependencies

Using [Poetry][1] to manage the virtual environment and packages. I also highly recommend using [Pyenv][2] to install and manage your python interpreters.

This script uses [pyautogui][3] for clicking and [Typer][4] for CLI parsing.

## Installation

TODO: Work in Progress (still figuring out packaging and installation.)

## Development

TODO: Fix this section

## Testing

This project utilizes [pytest][5] and [pytest-mock][6]. Both should be included in pyproject.toml dev dependencies, and `.vscode/settings.json` should already be setup to use these libraries.

Please type annotate any mocks used, which should be `MockerFixture` if you use pytest-mock.

## Scripts

```bash
# define your local python version
pyenv local 3.9.6
```

```bash
# install all deps from pyproject.toml
poetry install
```

```bash
# activate virtual environment first
poetry shell
# run tests, also outputs code coverage
python -m pytest -v --cov=clickpy --capture=sys tests/
```

```bash
# run this to generate report
coverage html
```

```bash
# open html coverage doc, windows doesn't have open.
[ -x "$(command -v open)" ] && open htmlcov/index.html || start htmlcov/index.html
```

```sh
# same command for fish shell
[ -x (command -v open) ] && open htmlcov/index.html || start htmlcov/index.html
```

[1]: https://github.com/python-poetry/poetry
[2]: https://github.com/pyenv/pyenv
[3]: https://github.com/asweigart/pyautogui
[4]: https://github.com/tiangolo/typer
[5]: https://github.com/pytest-dev/pytest
[6]: https://github.com/pytest-dev/pytest-mock

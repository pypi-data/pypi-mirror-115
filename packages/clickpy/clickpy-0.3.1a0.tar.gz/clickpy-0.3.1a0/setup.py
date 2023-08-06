# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clickpy']

package_data = \
{'': ['*']}

install_requires = \
['PyAutoGUI>=0.9.53,<0.10.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['clickpy = clickpy:run']}

setup_kwargs = {
    'name': 'clickpy',
    'version': '0.3.1a0',
    'description': 'Automated mouse clicking script',
    'long_description': '# clickpy\n\nAutomated mouse clicker script.\n\n## Dependencies\n\nUsing [Poetry][1] to manage the virtual environment and packages. I also highly recommend using [Pyenv][2] to install and manage your python interpreters.\n\nThis script uses [pyautogui][3] for clicking and [Typer][4] for CLI parsing.\n\n## Installation\n\nTODO: Work in Progress (still figuring out packaging and installation.)\n\n## Development\n\nTODO: Fix this section\n\n## Testing\n\nThis project utilizes [pytest][5] and [pytest-mock][6]. Both should be included in pyproject.toml dev dependencies, and `.vscode/settings.json` should already be setup to use these libraries.\n\nPlease type annotate any mocks used, which should be `MockerFixture` if you use pytest-mock.\n\n## Scripts\n\n```bash\n# define your local python version\npyenv local 3.9.6\n```\n\n```bash\n# install all deps from pyproject.toml\npoetry install\n```\n\n```bash\n# activate virtual environment first\npoetry shell\n# run tests, also outputs code coverage\npython -m pytest -v --cov=clickpy --capture=sys tests/\n```\n\n```bash\n# run this to generate report\ncoverage html\n```\n\n```bash\n# open html coverage doc, windows doesn\'t have open.\n[ -x "$(command -v open)" ] && open htmlcov/index.html || start htmlcov/index.html\n```\n\n```sh\n# same command for fish shell\n[ -x (command -v open) ] && open htmlcov/index.html || start htmlcov/index.html\n```\n\n[1]: https://github.com/python-poetry/poetry\n[2]: https://github.com/pyenv/pyenv\n[3]: https://github.com/asweigart/pyautogui\n[4]: https://github.com/tiangolo/typer\n[5]: https://github.com/pytest-dev/pytest\n[6]: https://github.com/pytest-dev/pytest-mock\n',
    'author': 'fitzlang',
    'author_email': 'fitzlang1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fitzlang/clickpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

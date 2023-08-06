# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_mailman', 'flask_mailman.backends']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.15.2,<0.16.0',
         'mkdocs-autorefs>=0.2.1,<0.3.0'],
 'test': ['black>=21.5b2,<22.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=2.12.0,<3.0.0']}

setup_kwargs = {
    'name': 'flask-mailman',
    'version': '0.3.0',
    'description': "Porting Django's email implementation to your Flask applications.",
    'long_description': "# Flask-Mailman\n\n![PyPI](https://img.shields.io/pypi/v/flask-mailman?color=blue)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/flask-mailman?color=brightgreen)\n[![dev workflow](https://github.com/waynerv/flask-mailman/actions/workflows/dev.yml/badge.svg?branch=master)](https://github.com/waynerv/flask-mailman/actions/workflows/dev.yml)\n![GitHub commits since latest release (by SemVer)](https://img.shields.io/github/commits-since/waynerv/flask-mailman/latest?color=cyan)\n![PyPI - License](https://img.shields.io/pypi/l/flask-mailman?color=blue)\n\nFlask-Mailman is a Flask extension providing simple email sending capabilities.\n\nIt was meant to replace unmaintained Flask-Mail with a better warranty and more features.\n\n## Usage\n\nFlask-Mail ported Django's email implementation to your Flask applications, which may be the best mail sending implementation that's available for python.\n\nThe way of using this extension is almost the same as Django.\n\nDocumentation: https://waynerv.github.io/flask-mailman.\n\n**Note: A few breaking changes have been made in v0.2.0 version** to ensure that API of this extension is basically the same as Django.\nUsers migrating from Flask-Mail should upgrade with caution.\n\n## Credits\n\nThanks to [Jetbrains](https://jb.gg/OpenSource) for providing an Open Source license for this project.\n\n[![Jetbrains Logo](docs/img/jetbrains-variant-4.png)](www.jetbrains.com)\n\nBuild tools and workflows of this project was inspired by [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n",
    'author': 'Waynerv',
    'author_email': 'ampedee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/waynerv/flask-mailman',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

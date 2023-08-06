# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cutepandas',
 'cutepandas.constants',
 'cutepandas.pandasmodels',
 'cutepandas.pandaswidgets',
 'cutepandas.util']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.0,<2.0.0', 'prettyqt>=0,<1']

extras_require = \
{'pyqt6': ['PyQt6>=6.2,<7.0',
           'PyQt6-Charts>=6.2,<7.0',
           'PyQt6-WebEngine>=6.2,<7.0',
           'PyQt6-QScintilla>=2.0,<3.0'],
 'pyside6:python_version < "3.11"': ['pyside6>=6.2,<7.0']}

setup_kwargs = {
    'name': 'cutepandas',
    'version': '0.2.2',
    'description': 'Qt Widgets and Objects for Pandas datastructures',
    'long_description': '# cutepandas: Pythonic layer on top of PyQt5 / PySide2 / PySide6\n[![PyPI Latest Release](https://img.shields.io/pypi/v/cutepandas.svg)](https://pypi.org/project/cutepandas/)\n[![Package Status](https://img.shields.io/pypi/status/cutepandas.svg)](https://pypi.org/project/cutepandas/)\n[![License](https://img.shields.io/pypi/l/cutepandas.svg)](https://github.com/phil65/CutePandas/blob/master/LICENSE)\n[![Travis Build Status](https://travis-ci.org/phil65/cutepandas.svg?branch=master)](https://travis-ci.org/phil65/cutepandas)\n[![CodeCov](https://codecov.io/gh/phil65/CutePandas/branch/master/graph/badge.svg)](https://codecov.io/gh/phil65/CutePandas)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyUp](https://pyup.io/repos/github/phil65/CutePandas/shield.svg)](https://pyup.io/repos/github/phil65/CutePandas/)\n\n## What is it?\n\n**CutePandas** is a Python package that provides Qt-based widgets related to pandas data structures.\n\n## Main Features\n\nToDo.\n\n   [pandaswidgets]: https://phil65.github.io/CutePandas/pandaswidgets.html\n\n\n## Where to get it\nThe source code is currently hosted on GitHub at:\nhttps://github.com/phil65/CutePandas\n\nThe latest released version are available at the [Python\npackage index](https://pypi.org/project/cutepandas).\n\n```sh\n# or PyPI\npip install cutepandas\n```\n\n## Dependencies\n- [orjson](https://pypi.org/project/orjson)\n\n\n## Installation from sources\n\nThis project uses poetry for dependency management and packaging. Install this first.\nIn the `cutepandas` directory (same one where you found this file after\ncloning the git repo), execute:\n\n```sh\npoetry install\n```\n\n## License\n[MIT](LICENSE)\n\n## Documentation\nThe official documentation is hosted on Github Pages: https://phil65.github.io/CutePandas/\n\n## Contributing to cutepandas [![Open Source Helpers](https://www.codetriage.com/phil65/cutepandas/badges/users.svg)](https://www.codetriage.com/phil65/cutepandas)\n\nAll contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.\n\nOr maybe through using CutePandas you have an idea of your own or are looking for something in the documentation and thinking ‘this can be improved’...you can do something about it!\n',
    'author': 'phil65',
    'author_email': 'philipptemminghoff@googlemail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/phil65/cutepandas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

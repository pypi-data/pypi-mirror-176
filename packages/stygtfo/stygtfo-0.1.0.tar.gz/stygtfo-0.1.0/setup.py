# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stygtfo']

package_data = \
{'': ['*']}

install_requires = \
['diff-pdf-visually>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['stygtfo = stygtfo:main']}

setup_kwargs = {
    'name': 'stygtfo',
    'version': '0.1.0',
    'description': 'A simple tool to comment out packages not used in a latex document',
    'long_description': '# stygtfo\nA simple tool to comment out packages not used in a latex document.\n\nWhy? Because I usually experiment with packages a lot and in the end I don\'t use them all, but it\'s basically impossible to know which ones I don\'t use.\n\nThis pacakge compiles the document with every package commented out one by one, and compares the expected pdf output with the actual pdf output. If the pdf output is the same, the package is determined not used and commented out.\n\nThis package is not tested basically at all, and I only used tectonic to test it (beacuse the others are slow and don\'t garantee the packages are installed). It might not work with other engines. In fact, it probably won\'t. Maybe in the future I\'ll update it, but I doubt it. Fell free to fork it and make PRs.\n\n## Usage\n```bash\nstygtfo <pathToTexFile> [--output <outputfile>] [--engine <pathToEngine>] [--verbose <bool>] [--args <argsToPassToEngine>] [--temp <pathToTempDir>]\n```\nCurrently, the `--args` option is not implemented, if some interest is shown I\'m free to do it.\n\n\n```python\nimport stygtfo\nstygtfo.CheckUnusedPackages("path/to/file.tex", "path/to/engin", usedPackages=None, resultedPath=None, verbose=False, pathToTemp=None)\n```\n\n## Installation\n```bash\npip install --user stygtfo\n```\nYou will need the same requirements as [diff-pdf-visually](https://github.com/bgeron/diff-pdf-visually#how-to-install-this), which on Windows is ImageMagick and Poppler. You can get them on chocolatey too.\n\nI don\'t know if the `--user` flag is actually needed, but I had some problems with it, so I recommend using it (except if you\'re installing it in a virtualenv).',
    'author': 'notPlancha',
    'author_email': 'andre.plancha@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

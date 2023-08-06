# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eetlijst']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'pytz>=2022.6,<2023.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'python-eetlijst',
    'version': '2.0.0',
    'description': 'Unofficial Python API to interface with Eetlijst.nl',
    'long_description': "# Python-eetlijst\nUnofficial Python API for interfacing with Eetlijst.nl, a Dutch website used by\nstudents to manage dinner status and expenses.\n\n[![Linting](https://github.com/basilfx/python-eetlijst/actions/workflows/lint.yml/badge.svg)](https://github.com/basilfx/python-eetlijst/actions/workflows/lint.yml)\n[![Testing](https://github.com/basilfx/python-eetlijst/actions/workflows/test.yml/badge.svg)](https://github.com/basilfx/python-eetlijst/actions/workflows/test.yml)\n[![PyPI version](https://badge.fury.io/py/python-eetlijst.svg)](https://badge.fury.io/py/python-eetlijst)\n\nCurrent features include:\n\n* List all residents\n* Get the name of the list\n* Get or set the noticeboard\n* Get or set the dinner status\n\n## Installation\nTo install this module, run `pip install python-eetlijst` to install from Pip.\nIf you prefer to install the latest version from Github, use\n`pip install git+https://github.com/basilfx/python-eetlijst`.\n\n## Examples\nThree examples are included in the `examples/` folder. The purpose is to\ndemonstrate some functionality.\n\n### dinner.py\nPrint or set the current dinner status, in a terminal window. Run it with\n`python dinner.py <username> <password> get|set`.\n\nIt shall print something similar to this, when getting the current status:\n\n```\nDinner status for 2014-03-30. The deadline is 16:00:00, and has passed.\n\nIn total, 4 people (including guests) will attend diner.\n\nUnknown1 | Unknown2 | Unknown3 | Unknown4 | Unknown5\n   C     |  D + 2   |    X     |    X     |    ?\n\nX = No, C = Cook, D = Dinner, ? = Unknown\n```\n\n### noticeboard.py\nView or change the current noticeboard. Run it with\n`python noticeboard.py <username> <password> get|set`.\n\n### session.py\nGiven a session id, print the name of the Eetlijst list. Run it with\n`python session.py <session_id>`\n\n## Contributing\nSee the [`CONTRIBUTING.md`](CONTRIBUTING.md) file.\n\n## Tests\nCurrently, a minimal set of tests have been written. These tests only verify\nthe 'scraping' functionality and correct sesision handling, by faking\nresponses. However, they do not test any submit functionality, since it would\nrequire an active connection with Eetlijst.nl during the tests.\n\nTo run the tests, please clone this repository and run `poetry run pytest`.\n\n## Documentation\nThis is future work :-)\n\nFor now, please look at the source code, the tests and the examples.\n\n## License\nSee the [`LICENSE.md`](LICENSE.md) file (GPLv3 license). You may change the\ncode freely, but any change must be made available to the public.\n\n## Disclaimer\nUse this library at your own risk. I cannot be held responsible for any\ndamages.\n\nThis page and its content is not affiliated with Eetlijst.nl.\n",
    'author': 'Bas Stottelaar',
    'author_email': 'basstottelaar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/basilfx/python-eetlijst',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

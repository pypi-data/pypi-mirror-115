# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perceval', 'perceval.backends', 'perceval.backends.zulip', 'tests']

package_data = \
{'': ['*'], 'tests': ['data/zulip/*']}

install_requires = \
['grimoirelab-toolkit', 'perceval', 'requests>=2.7.0,<3.0.0']

setup_kwargs = {
    'name': 'perceval-zulip',
    'version': '0.1.0',
    'description': 'Bundle of Perceval backends for Zulip.',
    'long_description': '# perceval-zulip [![Build Status](https://github.com/vchrombie/grimoirelab-perceval-zulip/workflows/tests/badge.svg)](https://github.com/vchrombie/grimoirelab-perceval-zulip/actions?query=workflow:tests+branch:master+event:push) [![Coverage Status](https://img.shields.io/coveralls/vchrombie/grimoirelab-perceval-zulip.svg)](https://coveralls.io/r/vchrombie/grimoirelab-perceval-zulip?branch=master) [![PyPI version](https://badge.fury.io/py/perceval-zulip.svg)](https://badge.fury.io/py/perceval-zulip)\n\nBundle of Perceval backends for Zulip.\n\n## Backends\n\nThe backends currently managed by this package support the next repositories:\n\n* Zulip\n\n## Requirements\n\n* Python >= 3.6\n* python3-requests >= 2.7\n* grimoirelab-toolkit >= 0.2\n* perceval >= 0.17.4\n\n## Installation\n\n### Getting the source code\n\nClone the repository\n```\n$ git clone https://github.com/vchrombie/grimoirelab-perceval-zulip\n```\n\n### Prerequisites\n\n#### Poetry\n\nWe use [Poetry](https://python-poetry.org/docs/) for managing the project.\nYou can install it following [these steps](https://python-poetry.org/docs/#installation).\n\n### Installation and configuration\n\nInstall the required dependencies (this will also create a virtual environment)\n```\n$ poetry install\n```\n\nActivate the virtual environment\n```\n$ poetry shell\n```\n\n## Examples\n\n### Zulip\n\n**Note:** You need the `email` and the `api_token` from the server. You can create a bot and use it for the authentication,\nplease read the docs at [About bots (Zulip Help Center)](https://zulip.com/help/bots-and-integrations).\n\nFetch messages from the `importlib` stream of the [Python Zulip Server](https://python.zulipchat.com)\n```\n$ perceval zulip https://python.zulipchat.com importlib -e bot@zulipchat.com -t xxxx\n```\n\n## Contributing\n\nThis project follows the [contributing guidelines](https://github.com/chaoss/grimoirelab/blob/master/CONTRIBUTING.md)\nof the GrimoireLab.\n\nAdhering to the guidelines, the work is started in this external repository. But, this can be merged\n([chaoss/grimoirelab-perceval/#/667](https://github.com/chaoss/grimoirelab-perceval/pull/667)) into the \n[Perceval](https://github.com/chaoss/grimoirelab-perceval) repository in the future.\n\n## License\n\nLicensed under GNU General Public License (GPL), version 3 or later.\n',
    'author': 'GrimoireLab Developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://chaoss.github.io/grimoirelab/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

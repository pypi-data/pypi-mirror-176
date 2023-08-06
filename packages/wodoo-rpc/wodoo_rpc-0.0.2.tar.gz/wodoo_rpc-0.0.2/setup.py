# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wodoo_rpc', 'wodoo_rpc.importers']

package_data = \
{'': ['*']}

install_requires = \
['OdooRPC>=0.8.0,<0.9.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pylint-gitlab>=1.1.0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.25.1,<3.0.0',
 'wodoo-datalib>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'wodoo-rpc',
    'version': '0.0.2',
    'description': 'Helper Functions around OdooRPC',
    'long_description': '# Wodoo-RPC\n\nSeveral Abstraction layers around [OdooRPC](https://odoorpc.readthedocs.io/en/latest/).\n\nMade Possible by: [WEMPE Elektronic GmbH](https://wetech.de)\n\n## Features\n\n- Login to Odoo helper functions\n- Importing Images from the Filesystem\n- Import CSV/Json/Excel Data to Odoo via RPC\n- Import res.config.settings\n- import Translations\n- Extend Base.Import feature with Language cols (fieldname:lang:en_US, fieldname:lang:de_DE)\n- Copy Records from Odoo to Odoo via RPC and remap relational Atributes\n\n## Development\n\n### VS Code Devcontainer\n\nThis workspace contains a [Vscode devcontainer](https://code.visualstudio.com/docs/remote/containers).\n\n## Gitlab Release\n\nThere are 2 Ways to start a release Pipeline:\n\n1. Via gitlab UI\n   1. Create new Pipeline in CI View\n   2. Supply Variables "`BUMP_TARGET`" [Valid Values](https://python-poetry.org/docs/cli/#version) and optional "`TAG_NOTE`" to add a text to the Git Tag.\n   3. Profit\n2. Via Git while Pushing\n   - Publish a path release: `git push -o ci.variable="BUMP_TARGET=patch"`\n   - Major release with release comment `git push -o ci.variable="BUMP_TARGET=patch" -o ci.variable="TAG_NOTE=This is a super cool new version"`\n',
    'author': 'Joshua Kreuder',
    'author_email': 'joshua_kreuder@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/joshuader6/wodoo-rpc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

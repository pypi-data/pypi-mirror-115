# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imia']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'imia',
    'version': '0.2.0',
    'description': 'Full stack authentication library for ASGI.',
    'long_description': '# Imia\n\nImia (belarussian for "a name") is an authentication library for Starlette and FastAPI (python 3.8+).\n\n![PyPI](https://img.shields.io/pypi/v/imia)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/alex-oleshkevich/imia/Lint)\n![GitHub](https://img.shields.io/github/license/alex-oleshkevich/imia)\n![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/imia)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/imia)\n![GitHub Release Date](https://img.shields.io/github/release-date/alex-oleshkevich/imia)\n![Lines of code](https://img.shields.io/tokei/lines/github/alex-oleshkevich/imia)\n\n## Installation\n\nInstall `imia` using PIP or poetry:\n\n```bash\npip install imia\n# or\npoetry add imia\n```\n\n## Features\n\n- Login/logout flows\n- Pluggable authenticators:\n    - WWW-Basic\n    - session\n    - token\n    - bearer token\n    - any token (customizable)\n    - API key\n- Database agnostic user storage\n- Authentication middleware\n    - with fallback strategies:\n        - redirect to an URL\n        - raise an exception\n        - do nothing\n    - with optional URL protection\n    - with option URL exclusion from protection\n- User Impersonation (stateless and stateful)\n- [WIP] Remember me\n- [WIP] Two-Factor flow\n\n## Quick start\n\nIf you are too lazy to read this doc, take a look into `examples/` directory. There you will find several files demoing\nvarious parts of this library.\n\n## Docs\n\n1. [Configuration](docs/configuration.md)\n2. [Login/Logout flow](docs/login_logout.md)\n3. [User token](docs/user_token.md)\n4. [Request authentication](docs/authentication.md)\n5. [Authenticators](docs/authenticators.md)\n6. [User impersontation](docs/impersonation.md)\n\n## Usage\n\nSee [examples/](examples) directory.\n',
    'author': 'Alex Oleshkevich',
    'author_email': 'alex.oleshkevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alex-oleshkevich/imia',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)

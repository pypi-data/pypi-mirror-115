# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daeclipse', 'daeclipse.models']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.7.1,<5.0.0',
 'browser-cookie3>=0.12.1,<0.13.0',
 'cli-ui>=0.14.1,<0.16.0',
 'html-to-draftjs>=1.0.1,<2.0.0',
 'pick>=1.0.0,<2.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'requests>=2.26.0,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'daeclipse',
    'version': '0.1.0',
    'description': 'A Python library for DeviantArt Eclipse functionality',
    'long_description': '# dAEclipse\n[![PyPI](https://img.shields.io/pypi/v/daeclipse)](https://pypi.org/project/daeclipse/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/daeclipse)](https://pypi.org/project/daeclipse/) [![PyPI - License](https://img.shields.io/pypi/l/daeclipse)](https://github.com/Pepper-Wood/daeclipse/blob/main/LICENSE)\n\n[daeclipse](https://pypi.org/project/daeclipse/) is a reverse-engineered Python library for DeviantArt Eclipse functionality.\n\nThis repo also contains a handy CLI to expose and test `daeclipse` capabilities.\n\n```bash\npython3 cli.py --help\n```\n```\nUsage: cli.py [OPTIONS] COMMAND [ARGS]...\n\n  DeviantArt Eclipse CLI\n\nOptions:\n  --install-completion  Install completion for the current shell.\n  --show-completion     Show completion for the current shell, to copy it or\n                        customize the installation.\n\n  --help                Show this message and exit.\n\nCommands:\n  add-art-to-groups  Submit DeviantArt deviation to groups.\n  hot-tags           Return top tags on the hottest deviations.\n  post-status        Post a DeviantArt status.\n  show-tags          Return list of tags for given deviation.\n  user-comments      Retrieve recent comments made by specified user.\n```\n\n## Installation\n\nThe Python library is available via https://pypi.org/project/daeclipse/\n\n```bash\npip install daeclipse\n```\n\nThe CLI is only available by downloading / cloning the repo to your local machine:\n\n```bash\ngit clone git@github.com:Pepper-Wood/daeclipse.git\n```\n\n## Usage\n\n```py\nimport daeclipse\n\n# Fetches a list of group names the user is a member of.\n# You will need to be logged into DeviantArt and have a chrome page open.\neclipse = daeclipse.Eclipse()\ngroups, has_more, next_offset, total = eclipse.get_groups("Pepper-Wood", 0)\nfor group in groups:\n    print(group.username)\n```\n\n## Build Status and Checks\n\nCICD is run thorugh GitHub Actions and makes the below checks on the two components of this repository:\n\n| | Python Package | OpenAPI Spec |\n| --- | --- | --- |\n| Lint | ![Python Linter Workflow Status](https://github.com/Pepper-Wood/daeclipse/actions/workflows/linter-python.yml/badge.svg) | ![OpenAPI Linter Workflow Status](https://github.com/Pepper-Wood/daeclipse/actions/workflows/linter-openapi.yml/badge.svg) |\n| Test | Coming Soon... | Coming soon... |\n| Deploy | ![PyPI Package Workflow Status](https://github.com/Pepper-Wood/daeclipse/actions/workflows/pypi.yml/badge.svg) | ![GitHub Pages Workflow Status](https://github.com/Pepper-Wood/daeclipse/actions/workflows/gh-pages.yml/badge.svg) |\n\n## Contributing\n\nContributions are always welcome, no matter how large or small! Before contributing, please read the [code of conduct](CODE_OF_CONDUCT.md).\n\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)\n\nIf you have a feature request, run into a bug, or are unsure about anything, feel free to submit a GitHub issue.\n\nIf you are interested in creating a Pull Request, please read the [guide on this repository\'s development process](docs/development.md).\n\nCommit titles on the `main` branch follow the [emoji-commit-messages](https://github.com/cooperka/emoji-commit-messages) naming convention.\n\n## Caveats / Disclaimer\n\nDeviantArt\'s history as a website is storied. Prior to the release of Eclipse, there were two options with creating tooling around its UI:\n- The [Public DeviantArt API](https://www.deviantart.com/developers/). See [accompanying Python wrapper](https://pypi.org/project/deviantart/). The API is relatively easy to use - and utilizes OAuth2 for authentication - but its endpoints and functionality are sparce. It also was not updated for some time but now appears to be getting a handful of new endpoints based on the changelog.\n- The internal [DeviantArt Interactive Fragment Interface (DiFi)](https://github.com/danopia/deviantart-difi/wiki). DiFi has a wide range of functionality but is volatile/unreliable and difficult to use - especially compared to modern APIs.\n\nOn October 2019, DeviantArt announced [DeviantArt Eclipse](https://www.deviantart.com/team/journal/DeviantArt-Eclipse-is-Here-814629875), a new UI (mostly) built in React. There are still a handful of pages on the website that expose the old website (i.e. https://www.deviantart.com/groups/) where functionality hasn\'t been completely ported. But with the new React UI, DeviantArt brought along a third option for tooling:\n- The internal **DeviantArt NAPI**, currently undocumented. The structure of its endpoints resembles RESTful practices, and authentication is done through scraping a CSRF token on the website or using a user\'s stored `.deviantart.com` cookies.\n\nThe implementation in this library relies on the DeviantArt NAPI. As such, functionality may break without warning depending on whether the internal DeviantArt team makes changes to these endpoints.\n',
    'author': 'Kathryn DiPippo',
    'author_email': 'dipippo.k@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://kathryndipippo.com/daeclipse/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)

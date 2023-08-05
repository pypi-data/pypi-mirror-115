# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autopr']

package_data = \
{'': ['*']}

install_requires = \
['click',
 'marshmallow',
 'marshmallow-dataclass',
 'pygithub',
 'pyyaml',
 'single-source>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['auto-pr = autopr:main']}

setup_kwargs = {
    'name': 'auto-pr',
    'version': '1.0.1',
    'description': 'Perform bulk updates across repositories',
    'long_description': '<img width="128" src="https://github.com/getyourguide/auto-pr/raw/master/img/logo.svg" alt="auto-pr logo" />\n\n![CI](https://github.com/getyourguide/auto-pr/workflows/CI/badge.svg)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7db0700cf0b74ac6976e520fbdb92a7f)](https://www.codacy.com/gh/getyourguide/auto-pr/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=getyourguide/auto-pr&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/7db0700cf0b74ac6976e520fbdb92a7f)](https://www.codacy.com/gh/getyourguide/auto-pr/dashboard?utm_source=github.com&utm_medium=referral&utm_content=getyourguide/auto-pr&utm_campaign=Badge_Coverage)\n[![PyPI version](https://badge.fury.io/py/auto-pr.svg)](https://badge.fury.io/py/auto-pr)\n![PyPI downloads](https://img.shields.io/pypi/dm/auto-pr)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# auto-pr\n\nA command line tool to perform bulk updates across multiple GitHub repositories.\n\n## How to install\n\nWith [pipx](https://pipxproject.github.io/pipx/) (recommended):\n\n```bash\npipx install auto-pr\n```\nWith pip:\n\n```bash\npip install auto-pr\n```\n\n## Usage\n\n[![Usage](https://github.com/getyourguide/auto-pr/raw/master/img/workflow.svg)](https://github.com/getyourguide/auto-pr/raw/master/img/workflow.svg)\n\n### Init\n\nFirst initialise the project directory by running the `init` command within an empty directory.\n\n```bash\nauto-pr init --api-key=<github_token> --ssh-key-file=<path-to-ssh-key>\n```\n\nWhere `<github_token>` is a GitHub [personal access token](https://github.com/settings/tokens) which has `repo` and `user:user:email` scope.\n\nNext modify the generated `config.yaml` file with your desired configurations.\n\n```yaml\ncredentials:\n  api_key: <github_token>\n  ssh_key_file: /path/to/ssh/key/to/push/.ssh/id_rsa\npr:\n  body: >\n    Body of the PR that will be generated\n\n    Can be multi-line :)\n  branch: auto-pr # The branch name to use when making changes\n  message: Replace default pipelines with modules # Commit message\n  title: \'My awesome change\' # Title of the PR\nrepositories: # Rules that define what repos to update\n  - mode: add\n    match_owner: <org/user>\nupdate_command:\n  - touch\n  - my-file\n```\n\n### Repositories\n\nYou can define the list of repositories to pull and build into the database to update using a list of rules.\n\n-   `mode` - either `add` or `remove` - used to either match or negate\n-   `public` (optional) - pull only public or private, leave out for both\n-   `archived` (optional) -  archived or non-archived, leave out for both\n-   `match_owner` (optional) - the owner or user to pull\n-   `match_name` (optional) - a list of regular expressions to match against to pull\n\nThe flags of the filter rules are optional not specifying will run the command on all repositories that the token has access too.\n\n### Update Command\n\nThis is the list containing the command to be executed along with the arguments passed to it. It will be executed from\nthe root of each repository that is processed.\n\nIf an error occurs during the execution it will be displayed in the output but will not halt the execution.\n\nSee [example commands](docs/examples.md#commands)\n\n### Pull\n\nAfter you have configured the project you can now pull the repositories down that match your rules.\n\n```bash\nauto-pr pull\n```\n\nThis will generate a `db.json` file within your workdir containing a list of mapped repositories and their state.\n\nThis command can be run multiple times, if there are new matching repositories found they will be merged into the existing database.\n\n### Test\n\nOnce the `pull` command has finished setting up the work directory you can now run test to check what the changes that will be made by the script will yield.\n\n### Run\n\nWhen you\'re confident with the changes output from the `test` command you can finally execute `run`.\n\n```bash\nauto-pr run\n```\n\nThis will perform the changes to a branch on the locally cloned repository and push the branch upstream with the information you provided within `config.yaml`.\n\nSee `--help` for more information about other commands and their  usage.\n\n## Security\n\nFor sensitive security matters please contact [security@getyourguide.com](mailto:security@getyourguide.com).\n\n## Legal\n\nCopyright 2021 GetYourGuide GmbH.\n\nauto-pr is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full text.\n',
    'author': 'GetYourGuide GmbH',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/getyourguide/auto-pr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

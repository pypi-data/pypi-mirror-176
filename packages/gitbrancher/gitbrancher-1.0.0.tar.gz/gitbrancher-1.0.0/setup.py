# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['gitbrancher']
entry_points = \
{'console_scripts': ['brancher = gitbrancher:main']}

setup_kwargs = {
    'name': 'gitbrancher',
    'version': '1.0.0',
    'description': 'Manage git workflow between multiple branches',
    'long_description': '# Brancher\n\nBrancher is a tool inspired by git flow that is more flexible in how it handles branching. It allows any configuration of branches and simply makes it easier to see which commits are in what branch, as well as advancing changes between branches. A typical branch layout may be like this:\n\n```\n┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐\n│     develop     ├──▶│     staging     ├──▶│      beta       ├──▶│     master*     │\n└─────────────────┘   └─────────────────┘   └─────────────────┘   └─────────────────┘\n\n                                                                 *production branch\n```\n\n**Note**: Brancher can handle other configurations, assuming there\'s one final "production" branch and any number of sequential pre-production branches to the left of it.\n\n## Installation\n\n(TODO)\n\n## Available Commands\n\nCommands:\n\n- overview (o): Prints an overview of branches with outstanding commits\n- forward (f): Fast forwards commits into branch\n- backfix (b): Applies changes on more advanced branches to current one\n- init: Initialize repo\n\nAdd `-h` to any command for usage details.\n\n## Usage\n\n### Initialization\nLet\'s start with an example of an empty repo.\n\n![First Commit](docs/ss-01-first-commit.png)\n\nNext, initialize Brancher. Brancher will store your branching model in your repository\'s local configuration.\n\n![Brancher init](docs/ss-02-init.png)\n\n### Advancing commits\n\nNow let\'s start some development work.\n\n![Development work](docs/ss-03-dev-work.png)\n\nThat looks good, so we\'ll advance that commit to `staging`, the next branch after `develop`.\n\n![Advancing commits](docs/ss-04-forward.png)\n\nWhile `staging` is having some Q/A work done, we\'ll continue development in `develop`:\n\n![More development work](docs/ss-05-more-dev-work.png)\n\n### Commit overview\n\nWith pending commits in `develop` and `staging`, let\'s get an overview of what commits exist where.\n\n![Overview](docs/ss-06-overview.png)\n\n### Backfilling hotfixes\n\nWith development work ongoing and Q/A happening on `staging`, let\'s make an urgent bugfix to production. As you can see, once that commit has been made, it only exists on the `master` branch, not other branches.\n\n![Hotfix to production](docs/ss-07-hotfix.png)\n\nWe want to bring that hotfix back into `develop`. After checking out `develop`, we\'ll apply the hotfix to develop too:\n\n![Backfix to staging](docs/ss-08-backfix.png)\n\nAn overview confirms that the backfilled changes have been applied to `develop`, but not `beta` or `staging`:\n\n![Overview hotfix](docs/ss-09-overview-hotfix.png)\n\nWe can remedy this by applying the hotfix to those environments, also:\n\n![Backfill beta](docs/ss-10-backfix-beta.png)\n\n![Backfill stagign](docs/ss-11-backfix-staging.png)\n\n',
    'author': 'Ken Kinder',
    'author_email': 'ken+github@kkinder.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

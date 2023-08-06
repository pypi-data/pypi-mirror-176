# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nba_api',
 'nba_api.library',
 'nba_api.library.debug',
 'nba_api.live',
 'nba_api.live.nba',
 'nba_api.live.nba.endpoints',
 'nba_api.live.nba.library',
 'nba_api.stats',
 'nba_api.stats.endpoints',
 'nba_api.stats.library',
 'nba_api.stats.static']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.2,<2.0.0', 'requests']

setup_kwargs = {
    'name': 'nba-api',
    'version': '1.1.14',
    'description': 'An API Client package to access the APIs for NBA.com',
    'long_description': "[![Version: PyPI](https://img.shields.io/pypi/v/nba_api.svg?longCache=true&style=for-the-badge&logo=pypi)](https://pypi.python.org/pypi/nba_api)\n[![Downloads per Month: PyPY](https://img.shields.io/pypi/dm/nba_api.svg?style=for-the-badge)](https://pepy.tech/project/nba-api)\n[![Build: CircleCI](https://img.shields.io/circleci/project/github/swar/nba_api.svg?style=for-the-badge&logo=circleci)](https://circleci.com/gh/swar/nba_api)\n[![License: MIT](https://img.shields.io/github/license/swar/nba_api.svg?style=for-the-badge)](https://github.com/swar/nba_api/blob/master/LICENSE)\n[![Slack](https://img.shields.io/badge/Slack-NBA_API-4A154B?style=for-the-badge&logo=slack)](https://join.slack.com/t/nbaapi/shared_invite/zt-1ipsuai9j-GjZjuP9S2~Uczuny1t74zA)\n\n# nba_api\n\n## An API Client Package to Access the APIs of NBA.com\n\n`nba_api` is an API Client for `www.nba.com`. This package intends to make the APIs of [NBA.com](https://www.nba.com/) easily accessible and provide extensive documentation about them.\n\n# Getting Started\n\n`nba_api` requires Python 3.7+ along with the `requests` and `numpy` packages. While `panadas` is not required, it is required to work with Pandas DataFrames.\n\n```bash\npip install nba_api\n```\n\n## NBA Official Stats\n\n```python\nfrom nba_api.stats.endpoints import playercareerstats\n\n# Nikola Jokić\ncareer = playercareerstats.PlayerCareerStats(player_id='203999') \n\n# pandas data frames (optional: pip install pandas)\ncareer.get_data_frames()[0]\n\n# json\ncareer.get_json()\n\n# dictionary\ncareer.get_dict()\n```\n\n## NBA Live Data\n\n```python\nfrom nba_api.live.nba.endpoints import scoreboard\n\n# Today's Score Board\ngames = scoreboard.ScoreBoard()\n\n# json\ngames.get_json()\n\n# dictionary\ngames.get_dict()\n```\n\n## Additional Examples\n\n- [Requests/Response Options](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/examples.md#endpoint-usage-example)\n  - Proxy Support, Custom Headers, and Timeout Settings\n  - Return Types and Raw Responses\n- [Static Data Sets](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/examples.md#static-usage-examples)\n  - Reduce HTTP requests for common and frequently accessed player and team data.\n- [Jupyter Notebooks](https://github.com/swar/nba_api/tree/master/docs/examples)\n  - Practical examples in Jupyter Notebook format, including making basic calls, finding games, working with play-by-play data, and interacting with live game data.\n\n# Documentation\n\n- [Table of Contents](https://github.com/swar/nba_api/tree/master/docs/table_of_contents.md)\n- [Package Structure](https://github.com/swar/nba_api/tree/master/docs/package_structure.md)\n- [Endpoints](/docs/nba_api/stats/endpoints)\n- Static Data Sets\n  - [players.py](https://github.com/swar/nba_api/tree/master/docs/nba_api/stats/static/players.md)\n  - [teams.py](https://github.com/swar/nba_api/tree/master/docs/nba_api/stats/static/teams.md)\n\n# Join the Community\n## Slack\n\nJoin [Slack](https://join.slack.com/t/nbaapi/shared_invite/zt-1ipsuai9j-GjZjuP9S2~Uczuny1t74zA) to get help, help others, provide feedback, see amazing projects, participates in discussions, and collaborate with others from around the world.\n\n## Stack Overflow\n\nNot a Slack fan? No problem. Head over to [StackOverflow](https://stackoverflow.com/questions/tagged/nba-api). Be sure to tag your post with `nba-api`.\n\n# Contributing\n\n*See [Contributing to the NBA_API](https://github.com/swar/nba_api/blob/master/CONTRIBUTING.md) for complete details.*\n\n## Endpoints\n\nA significant purpose of this package is to continuously map and analyze as many endpoints on NBA.com as possible. The documentation and analysis of the endpoints and parameters in this package are some of the most extensive information available. At the same time, NBA.com does not provide information regarding new, changed, or removed endpoints.\n\nIf you find a new, changed, or deprecated endpoint, open a [GitHub Issue](https://github.com/swar/nba_api/issues)\n\n## Bugs\n\nEncounter a bug, [report a bug](https://github.com/swar/nba_api/issues).\n\n# License & Terms of Use\n\n## API Client Package\n\nThe `nba_api` package is Open Source with an [MIT License](https://github.com/swar/nba_api/blob/master/LICENSE).\n\n## NBA.com\n\nNBA.com has a [Terms of Use](https://www.nba.com/termsofuse) regarding the use of the NBA’s digital platforms.\n",
    'author': 'Swar Patel',
    'author_email': 'swar.m.patel@gmail.com',
    'maintainer': 'Swar Patel',
    'maintainer_email': 'swar.m.patel@gmail.com',
    'url': 'https://github.com/swar/nba_api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)

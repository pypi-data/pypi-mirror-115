# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiobungie', 'aiobungie.ext', 'aiobungie.internal', 'aiobungie.objects']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp==3.7.4.post0',
 'aredis==1.1.8',
 'attrs==21.2.0',
 'python-dateutil==2.8.2']

setup_kwargs = {
    'name': 'aiobungie',
    'version': '0.2.5b4',
    'description': 'A small async api wrapper for the bungie api',
    'long_description': '<div align="center">\n    <h1>aiobungie</h1>\n    <p>An Asynchronous statically typed API wrapper for the bungie API written in Python.</p>\n    <a href="https://codeclimate.com/github/nxtlo/aiobungie/maintainability">\n    <img src="https://api.codeclimate.com/v1/badges/09e71a0374875d4594f4/maintainability"/>\n    </a>\n    <a href="https://github.com/nxtlo/aiobungie/issues">\n    <img src="https://img.shields.io/github/issues/nxtlo/aiobungie"/>\n    </a>\n    <a href="http://python.org">\n    <img src="https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10dev-blue"/>\n    </a>\n    <a href="https://pypi.org/project/aiobungie/">\n    <img src="https://img.shields.io/pypi/v/aiobungie?color=green"/>\n    </a>\n    <a href="https://github.com/nxtlo/aiobungie/blob/master/LICENSE">\n    <img src="https://img.shields.io/pypi/l/aiobungie"/>\n    </a>\n    <a href="https://github.com/nxtlo/aiobungie/blob/master/LICENSE">\n    <img src="https://img.shields.io/pypi/l/aiobungie"/>\n    </a>\n    <a href="https://www.codefactor.io/repository/github/nxtlo/aiobungie/">\n    <img src="https://www.codefactor.io/repository/github/nxtlo/aiobungie/badge">\n    </a>\n    <a href="https://github.com/nxtlo/aiobungie/actions/workflows/ci.yml">\n    <img src="https://github.com/nxtlo/aiobungie/actions/workflows/ci.yml/badge.svg?branch=master">\n    </a>\n    <a href="https://codeclimate.com/github/nxtlo/aiobungie/test_coverage"><img src="https://api.codeclimate.com/v1/badges/09e71a0374875d4594f4/test_coverage" /></a>\n\n</div>\n\n# Key Features\n\n* Fully Asynchronous.\n* Simplicity.\n* Efficient and optimized.\n* Statically typings and annotations.\n* All endpoints will be implemented.\n\n# Installing\n\nOfficial release.\n\n```s\n$ pip install aiobungie\n```\n\nDevelopment\n\n```s\n$ pip install git+https://github.com/nxtlo/aiobungie\n```\n\n## Quick Example\n\nSee [Examples for more.](https://github.com/nxtlo/aiobungie/tree/master/examples)\n\n```python\nimport aiobungie\n\nclient = aiobungie.Client(key=\'YOUR_API_KEY\')\n\nasync def main() -> None:\n\n    # fetch a clan from its id.\n    clan = await client.fetch_clan_from_id(1234)\n    # or fetch the clan by its name\n    clan = await client.fetch_clan("Fast")\n    print(f\'{clan.id}, {clan.name}, {clan.owner}, {clan.created_at}, {clan.about}\')\n\n    # fetch a destiny 2 player.\n    player = await client.fetch_player(\'Fate怒\')\n    print(f\'{player.name}, {player.id[0]}, {player.icon}, {player.type}\')\n\n    # fetch a specific character.\n    char = await client.fetch_character(player.id[0], aiobungie.MembershipType.STEAM, aiobungie.Class.WARLOCK)\n    print(f\'{char.emblem}, {char.light}, {char.id}, {char.race}, {char.gender}, {char._class}\')\n\n    # fetch activities.\n    activ = await client.fetch_activity(player.id[0], char.id, aiobungie.MembershipType.STEAM, aiobungie.GameMode.RAID)\n    print(\n        f\'\'\'{activ.mode}, {activ.kills}, {activ.player_count}, \n        {activ.duration}, {activ.when}, {activ.kd}, {activ.deaths},\n        {activ.assists}, {activ.hash} -> raids only {activ.raw_hash} -> Any\n        \'\'\')\n\n    # Raw search\n    endpoint = await client.from_path(\'User/.../.../\')\n    print(endpoint)\n\nclient.loop.run_until_complete(main())\n```\n\n### Requirements\n* Python >=3.8 -> Required.\n* aiohttp -> Required for http.\n* aredis -> Optional for cache.\n* attrs -> Class attrs.\n\n### Getting Help\n* Discord: `Fate 怒#0008` | `350750086357057537`\n* Docs: [Here](https://nxtlo.github.io/aiobungie/).\n',
    'author': 'nxtlo',
    'author_email': 'dhmony-99@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nxtlo/aiobungie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

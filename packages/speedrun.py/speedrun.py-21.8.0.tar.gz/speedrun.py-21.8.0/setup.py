# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['speedrunpy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0']

setup_kwargs = {
    'name': 'speedrun.py',
    'version': '21.8.0',
    'description': 'An asynchronous API wrapper for speedrun.com',
    'long_description': '# speedrun.py\n\nAn asynchronous API wrapper for speedrun.com\n\n## Coverage\n\n- [ ] Categories\n- [ ] Games\n- [ ] Guests\n- [ ] Leaderboards\n- [ ] Levels\n- [ ] Notifications\n- [ ] Platforms\n- [ ] Profile\n- [ ] Publishers\n- [ ] Regions\n- [ ] Runs\n- [ ] Series\n- [ ] Users\n- [ ] Variables\n',
    'author': 'null2264',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

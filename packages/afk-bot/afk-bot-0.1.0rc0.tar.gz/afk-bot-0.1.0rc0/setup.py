# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['afk_bot']

package_data = \
{'': ['*']}

install_requires = \
['PyAutoGUI>=0.9,<0.10', 'keyboard>=0.13,<0.14', 'typer>=0.7,<0.8']

entry_points = \
{'console_scripts': ['afk-bot = afk_bot.cli:main']}

setup_kwargs = {
    'name': 'afk-bot',
    'version': '0.1.0rc0',
    'description': 'A bot for the away from keyboard times',
    'long_description': '[![build](https://github.com/slickml/afk-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/slickml/afk-bot/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/slickml/afk-bot/branch/master/graph/badge.svg?token=Z7XP51MB4K)](https://codecov.io/gh/slickml/afk-bot)\n[![license](https://img.shields.io/github/license/slickml/afk-bot)](https://github.com/slickml/afk-bot/blob/master/LICENSE/)\n[![downloads](https://pepy.tech/badge/akf-bot)](https://pepy.tech/project/afk-bot)\n![pypi_version](https://img.shields.io/pypi/v/afk-bot)\n![python_version](https://img.shields.io/pypi/pyversions/afk-bot)\n\n\n\n<p align="center">\n  <a href="https://github.com/slickml/afk-bot">\n    <img src="https://raw.githubusercontent.com/slickml/afk-bot/master/assets/logo.png" width="250"></img>\n  </a>\n</p>\n\n<div align="center">\n<h1 align="center">AFK-Bot🤖: A bot for the away from keyboard times\n</h1>\n</div>\n\n## 🧠 Philosophy\nWe strongly believe that all developers should have full access to their resources (i.e. `sudo` access or permission to deactivate screens saver, ...). `afk-bot` 🤖 is a simple bot that moves the mouse cursor (every 1 second by default and it can be customized); so, your status never goes `Idle` and your screen never gets locked 😂 ...\n\n\n## 🛠 Installation\nTo begin with, you need to have a [Python version >=3.8](https://www.python.org) installed and to install the library\nfrom [PyPI](https://pypi.org/project/afk-bot/) simply run 🏃\u200d♀️ :\n```\n$ pip install afk-bot\n```\n\n## 📌 Quick Start\n`afk-bot` is a `command-line` based bot and you can simply run it in any `terminal` 🏃\u200d♀️ :\n```\n$ afk-bot                     <- runs the bot and the mouse cursor moves every 1 second by default\n\n$ afk-bot -t <interval-range> <- you can customize the interval with -t or --time\n\n$ afk-bot --help              <- shows the options \n```\nTo `exit`, simply press `CTRL+C` keys. \n\n## 📣 Common Issues\n  - Mac users should note that the accessibility to `Apple Events Server (AEServer)` should be turned on. Simply follow the steps 🏃\u200d♀️ :\n    ```\n    System Preferences > Security & Privacy > Choose Privacy Tab > Select Accessibility from Left Pane > Enable AEServer\n    ```\n  - Some Linux users might need to export the environment variable `DISPLAY`. Simply run 🏃\u200d♀️ :\n    ```\n    $ export DISPLAY=:0\n    ```\n## 🧑\u200d💻🤝 Contributing\nIf you think more features should be added, please open up an issue an. PRs are more than welcome 🙏 . You can find the details of the development process in our SlickML🧞 [Contributing](CONTRIBUTING.md) guidelines. We strongly believe that reading and following these guidelines will help us make the contribution process easy and effective for everyone involved 🚀🌙 .\n\n\n\n## ❓ 🆘 📲 Need Help?\nPlease join our [Slack Channel](https://www.slickml.com/slack-invite) to interact directly with the core team and our small community. This is a good place to discuss your questions and ideas or in general ask for help 👨\u200d👩\u200d👧 👫 👨\u200d👩\u200d👦 .\n\n',
    'author': 'Amirhessam Tahmassebi',
    'author_email': 'admin@slickml.com',
    'maintainer': 'Amirhessam Tahmassebi',
    'maintainer_email': 'admin@slickml.com',
    'url': 'https://www.slickml.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)

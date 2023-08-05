# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gitfix']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.18.1,<2.0.0', 'rich>=10.6.0,<11.0.0']

entry_points = \
{'console_scripts': ['gitfix = gitfix.main:main']}

setup_kwargs = {
    'name': 'gitfix',
    'version': '0.2.2',
    'description': 'Command-line tool to help you recover from a broken git state.',
    'long_description': '# GitFix\n\nTerminal application to help recover from a broken git state.\n\n## Screenshots\n\n![GitFix Screenshots](https://raw.githubusercontent.com/lucasmelin/gitfix/main/docs/assets/uncommitted.png?token=AABSHC7LZSRH6YORY6XWSB3BAXHY2)\n\n## Installation\n\nWith `pip`:\n```\npip install gitfix\n```\n\nWith `pipx`:\n```\npipx install gitfix\n```\n\nOptionally, see the releases page to download a binary for Windows. Rename the executable to `gitfix.exe` and add it to a directory in your `PATH`.\n\n## Acknowledgements\n\n- GitFixUm steps from https://sethrobertson.github.io/GitFixUm/, copyright © 2012 Seth Robertson, used under CC-BY-SA-3.0 with modifications.\n- Rich markdown table formatting from @aurium in https://github.com/googlefonts/fontbakery/pull/3227\n\n## Similar content\n- https://dangitgit.com/en\n- http://justinhileman.info/article/git-pretty/',
    'author': 'Lucas Melin',
    'author_email': 'lucas.melin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lucasmelin/gitfix',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['larkjs']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.11.1,<0.12.0']

entry_points = \
{'console_scripts': ['larkjs = larkjs.__main__:main']}

setup_kwargs = {
    'name': 'larkjs',
    'version': '0.0.2',
    'description': 'An extension to Lark that generates a Javascript standalone',
    'long_description': "# Lark.js - a port of the Lark parsing toolkit to Javascript\n\nLark is a parsing toolkit for Python, built with a focus on ergonomics, performance and modularity.\n\nWith Lark.js, you create a fast Javascript parser from a grammar written for Lark.\n\nThe compiled Javascript modules include Lark's base classes and utilities, such as `Tree`, `Transformer`, and `InteractiveParser`.\n\nCurrently, only LALR(1) is supported. (Earley support is planned!)\n\n### Quick links\n\n- [Lark (Python)](https://https://github.com/lark-parser/lark)\n- [Cheatsheet (PDF)](/docs/_static/lark_cheatsheet.pdf)\n- [Online IDE](https://lark-parser.github.io/ide)\n- [Gitter chat](https://gitter.im/lark-parser/Lobby)\n\n### Install Lark.js\n\n    $ pip install lark-js --upgrade\n\n[![Build Status](https://travis-ci.org/lark-parser/lark.svg?branch=master)](https://travis-ci.org/lark-parser/lark)\n\n### Generate a Javascript LALR(1) parser\n\n```bash\n\tpython -m lark-js my_grammar.lark -o my_parser.js\n```\n\nFor help, run:\n\n```bash\n\tpython -m lark-js --help\n```\n\n### Syntax Highlighting\n\nLark provides syntax highlighting for its grammar files (\\*.lark):\n\n- [Sublime Text & TextMate](https://github.com/lark-parser/lark_syntax)\n- [vscode](https://github.com/lark-parser/vscode-lark)\n- [Intellij & PyCharm](https://github.com/lark-parser/intellij-syntax-highlighting)\n- [Vim](https://github.com/lark-parser/vim-lark-syntax)\n- [Atom](https://github.com/Alhadis/language-grammars)\n\n\n## List of main features\n\n - Builds a parse-tree (AST) automagically, based on the structure of the grammar\n - **LALR(1)** parser - Fast and light\n - **EBNF** grammar\n - Usable in the browser and in Node\n - Automatic line & column tracking\n - Standard library of terminals (strings, numbers, names, etc.)\n - Import grammars from Nearley.js ([read more](/docs/tools.md#importing-grammars-from-nearleyjs))\n - And much more!\n\n## License\n\nLark.js uses the [MIT license](LICENSE).\n\n## Contribute\n\nLark.js is accepting pull-requests. If you would like to help, open an issue or find us on gitter.\n\n## Sponsoring\n\nLark.js was made possible with the help of a generous donation by [Smore](https://www.smore.com/) ❤️\n\nIf you like Lark, and want to see it grow, please consider [sponsoring us!](https://github.com/sponsors/lark-parser)\n",
    'author': 'Erez Shin',
    'author_email': 'erezshin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lark-parser/lark.js',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)

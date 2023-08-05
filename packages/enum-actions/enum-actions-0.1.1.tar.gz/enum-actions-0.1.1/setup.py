# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enum_actions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'enum-actions',
    'version': '0.1.1',
    'description': 'For easy selection command-line selection of an `enum.Enum` variant with `argparse.Action`s.',
    'long_description': '<div align="center">\n\n[![pypi](https://img.shields.io/pypi/v/enum-actions)](https://pypi.org/project/enum-actions/)\n[![github](https://img.shields.io/static/v1?label=&message=github&color=grey&logo=github)](https://github.com/aatifsyed/enum-actions)\n\n</div>\n\n# `enum-actions`\nFor easy selection command-line selection of an `enum.Enum` variant with `argparse.Action`s.\n\nUse it like this:\n```python\n>>> from enum_actions import enum_action\n>>> from argparse import ArgumentParser\n>>> import enum\n\n>>> class MyEnum(enum.Enum):\n...     A = 1\n...     B = 2\n\n>>> parser = ArgumentParser()\n>>> _ = parser.add_argument("-e", "--enum", action=enum_action(MyEnum), default="a", help="pick a variant") # create an action for your enum\n>>> args = parser.parse_args() # there will be an instance of MyEnum in the args object\n\n```\n\n## Features\n### Choices are handled transparently\n```text\nfoo.py --help\n\nusage: foo.py [-h] [-e {a,b}]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -e {a,b}, --enum {a,b}\n                        pick a variant (default: b)\n```\n\n### Defaults are handled transparently\nHaving a default string or enum will both work\n```python\nparser.add_argument("--enum", action=enum_action(MyEnum), default="a")\nparser.add_argument("--enum", action=enum_action(MyEnum), default=MyEnum.A)\n```\n',
    'author': 'Aatif Syed',
    'author_email': 'aatifsyedyp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aatifsyed/enum-actions',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

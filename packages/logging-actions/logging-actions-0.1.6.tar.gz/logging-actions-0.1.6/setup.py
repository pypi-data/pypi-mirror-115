# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logging_actions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'logging-actions',
    'version': '0.1.6',
    'description': 'For easy configuration of `logging.Logger`s with `argparse.Action`s.',
    'long_description': '<div align="center">\n\n[![pypi](https://img.shields.io/pypi/v/logging-actions)](https://pypi.org/project/logging-actions/)\n[![github](https://img.shields.io/static/v1?label=&message=github&color=grey&logo=github)](https://github.com/aatifsyed/logging-actions)\n\n</div>\n\n# `logging-actions`\nFor easy configuration of `logging.Logger`s with `argparse.Action`s.\n\nUse it like this:\n```python\n>>> from logging_actions import log_level_action\n>>> from argparse import ArgumentParser\n>>> import logging\n\n>>> logger = logging.getLogger("foo") # Create your script\'s logger\n>>> logger.addHandler(logging.StreamHandler())  # Don\'t forget to add a handler!\n\n>>> parser = ArgumentParser()\n>>> _ = parser.add_argument("--log-level", action=log_level_action(logger)) # create an action for your module\'s logger\n>>> args = parser.parse_args() # Your logger\'s level will be set for you when parsing\n\n```\n\n## Features\n### Choices are handled transparently\n```text\nfoo.py --help\n\nusage: foo.py [-h] [--log-level {critical,fatal,error,warn,warning,info,debug,notset}]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --log-level {critical,fatal,error,warn,warning,info,debug,notset}\n                        Set the logging level for foo.\n```\n\n### If you specify a default the log-level will be set accordingly\n```python\nparser.add_argument("-l", "--log-level", action=log_level_action(logger), default="info")\n```\n\n### Custom levels are supported\n```python\nlogging.addLevelName(5, "TRACE")\nparser.add_argument("-l", action=log_level_action(logger), default="trace")\n```\n\n## Benefits\n### A better logging pattern\nThis replaces the following pattern for setting script log levels\n```python\nfrom argparse import ArgumentParser\n\nparser = ArgumentParser()\nparser.add_argument(\n    "--log-level",\n    default=logging.INFO,\n    type=lambda x: getattr(logging, x)),\n    help="Configure the logging level.",\n)\nargs = parser.parse_args()\nlogging.basicConfig(level=args.log_level)\n```\n### Manage multiple loggers easily\n```python\nparser.add_argment("--foo-log-level", action=log_level_action(foo_logger))\nparser.add_argment("--bar-log-level", action=log_level_action(bar_logger))\n```',
    'author': 'Aatif Syed',
    'author_email': 'aatifsyedyp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aatifsyed/logging-actions',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flake8_action_hero', 'flake8_action_hero.actions']

package_data = \
{'': ['*']}

modules = \
['_flake8_action_hero_version']
install_requires = \
['flake8>=3.9.2,<4.0.0']

extras_require = \
{'package': ['importlib-metadata>=4.6.3,<5.0.0', 'packages>=0.1.0,<0.2.0']}

entry_points = \
{'flake8.extension': ['AH = flake8_action_hero.checker:ActionChecker']}

setup_kwargs = {
    'name': 'flake8-action-hero',
    'version': '0.1.0',
    'description': 'A plugin for flake8 that performs conditional FIXME/TODO checks.',
    'long_description': '# flake8-action-hero\nA plugin for flake8 that performs conditional FIXME/TODO checks.\n\n## Action Tags\n\nCode comments that begin with `# FIXME:`/`# TODO:` are often referred to as "FIXME Comments".  This plugin refers to them as action tags.\n\nAction tags are typically a tag followed by a series of commands and variables.  The series is defined by the module (action) handling the conditional test defined in sections below.\n\nThe parser for action tags attempts to be fairly flexible and allow for the following:\n\n```python\n\n# This will be ignored since there is no action.\n# FIXME: This is a bare fixme comment.\n# TODO: This is a bare todo comment.\n\n# This will be ignored since there is no action.\n# FIXME(SRS): This comment includes my initials and is a popular way to signify that a\n# person found an issue (and isn\'t directly responsible for fixing it).\n\n# This will be tested since there is a valid action.\n# FIXME(SRS): DATE: AFTER: 2022-01-01: This comment includes initials as well as a composite\n# action and condition and will be tested.\n\n# This will be ignored since no action handler exists (yet) for this.\n# CRITICAL: SCHRÖDINGER: CAT: DEAD: Do not commit while cat is dead.\n\n```\n\n### Date Conditional Action Tags\n\nExamples:\n\n```python\n# FIXME: DATE: AFTER: 2021-12-05: This will result in code `AH000: Date conditional action tag found (FIXME)\n```\n\n### Package Conditional Action Tags\n\nPackage conditional action tags attempt to locate and verify that a locally installed package is contained within a standard python packaging specifier.  This provides a utility to tag an area of code that may need to be refactored when a package is released (and locally available) that may contain a feature needed to bring in new functionality or prompt the need to refactor or remove a bugfix fixed upstream.\n\nExamples:\n\n```python\n# FIXME: PACKAGE: VERSION: aws-lambda-powertools>=0.19.0: New feature should remove following bandaid code.\n```\n\n```python\n# TODO: PACKAGE: VERSION: bungee-jump>=1.29: Can now jump with blindfold.  Add in new feature for blindfold jump.\n```\n\n```python\n# CRITICAL: PACKAGE: VERSION: orm-uber-tool>=2.12.0,<=2.12.5: Bug introduced in module will cause CPU to smoke. Danger.\n```\n\nUtilizing this tag requires that following dependencies:\n\n- [`packaging`](https://github.com/pypa/packaging): Developed by PyPa team and used in order to test a version against a specifier.\n- [`importlib_metadata`](https://github.com/python/importlib_metadata): Developed by Python team and used in order to find the most relevant installed package version within your python environment.\n\n## Error Codes\n\nIn the error code table the `{T}`/`{...}` represents a code and type related to the comment tag.  While 10 might be a short list it is most likely considered too long in most standards.  This project has opted to add in a few extras that don\'t directly overlap with other **fixme** related checkers as a way to offer some extended workflow and alerting functionality.\n\n<!-- TODO(SRS): AFTER: DATE: 2022-01-01: New years resolution: Add in descriptions of types and related history. -->\n\n| Code `{T}` | Type `{...}` | Description |\n|:----------:|:-------------|:------------|\n| `0` | `FIXME` | ... |\n| `1` | `TODO` | ... |\n| `2` | `XXX` | ... |\n| `3` | `BUG` | ... |\n| `4` | `REFACTOR` | ... |\n| `5` | `REMOVEME` | ... |\n| `6` | `LEGACY` | ... |\n| `7` | `CRITICAL` | ... |\n| `8` | `WARNING` | ... |\n\n| Error codes | Description | Utility |\n|:-----------:|:------------|:--------|\n| `AH00{T}` | Date after condition met (`{...}`) | Good for tracking feature dates. |\n| `AH01{T}` | Date before condition met (`{...}`) | Perhaps not very useful. |\n| `AH40{T}` | Package version specifier condition met (`{...}`) | Refactoring against upstream changes. |\n',
    'author': 'Shane Spencer',
    'author_email': '305301+whardier@users.noreply.github.com ',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whardier/flake8-action-hero',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

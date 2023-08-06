# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lintrunner_adapters',
 'lintrunner_adapters._common',
 'lintrunner_adapters.adapters',
 'lintrunner_adapters.tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

setup_kwargs = {
    'name': 'lintrunner-adapters',
    'version': '0.1.0',
    'description': 'Adapters and tools for lintrunner',
    'long_description': '# lintrunner-adapters\n\nAdapters for [lintrunner](https://github.com/suo/lintrunner)\n\n## Usage\n\n```text\nUsage: python -m lintrunner_adapters [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  run       Run an adapter.\n  to-sarif  Convert the output of lintrunner json (INPUT) to SARIF (OUTPUT).\n```\n',
    'author': 'Justin Chu',
    'author_email': 'justinchu@microsoft.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

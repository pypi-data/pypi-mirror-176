# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['boto3_utility_belt']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.24.45,<2.0.0', 'pyperclip>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'boto3-utility-belt',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jeremy Axmacher',
    'author_email': 'jeremy@obsoleter.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

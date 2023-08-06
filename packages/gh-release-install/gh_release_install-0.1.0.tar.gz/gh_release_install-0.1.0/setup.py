# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gh_release_install']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['gh-release-install = gh_release_install.cli:run']}

setup_kwargs = {
    'name': 'gh-release-install',
    'version': '0.1.0',
    'description': 'CLI helper to install Github releases on your system.',
    'long_description': None,
    'author': 'Joola',
    'author_email': 'jooola@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

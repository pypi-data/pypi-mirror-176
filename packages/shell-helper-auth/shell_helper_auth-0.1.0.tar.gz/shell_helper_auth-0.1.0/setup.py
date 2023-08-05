# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shell_helper_auth']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2,<3']

setup_kwargs = {
    'name': 'shell-helper-auth',
    'version': '0.1.0',
    'description': 'Requests authentication using shell helpers',
    'long_description': 'None',
    'author': 'Michal Porteš',
    'author_email': 'michalportes1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

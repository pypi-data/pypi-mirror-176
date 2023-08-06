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
    'version': '0.2.0',
    'description': 'Requests authentication using shell helpers',
    'long_description': '# Installation\n\n```\npip install shell-helper-auth\n```\n\n# Usage\n\nObjects of the class `ShellHelperAuth` are intended to be used as\nauthentication handlers as per the\n[Requests documentation](https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication).\n',
    'author': 'Michal Porteš',
    'author_email': 'michalportes1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mportesdev/shell-helper-auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

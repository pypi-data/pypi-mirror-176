# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_project_example_pypi']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'poetry-project-example-pypi',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'mpakdel-chwy',
    'author_email': 'mpakdel@chewy.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

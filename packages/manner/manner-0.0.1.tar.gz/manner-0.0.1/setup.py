# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manner']

package_data = \
{'': ['*']}

install_requires = \
['twine>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'manner',
    'version': '0.0.1',
    'description': 'Fast python linter.',
    'long_description': 'None',
    'author': 'zhivykh',
    'author_email': 'zivih.n@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

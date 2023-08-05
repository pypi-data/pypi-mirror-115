# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tex2tree']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0', 'networkx>=2.6.2,<3.0.0', 'ply>=3.11,<4.0']

setup_kwargs = {
    'name': 'tex2tree',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': '赵文祺',
    'author_email': '1027572886a@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

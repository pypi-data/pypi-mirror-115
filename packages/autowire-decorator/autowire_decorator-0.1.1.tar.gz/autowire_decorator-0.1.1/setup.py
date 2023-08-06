# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autowire_decorator']

package_data = \
{'': ['*']}

install_requires = \
['flask-restx>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'autowire-decorator',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'nadaabdelmaboud',
    'author_email': 'nada5aled52@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

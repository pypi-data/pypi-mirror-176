# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miller']

package_data = \
{'': ['*']}

install_requires = \
['amos>=0.1.10,<0.2.0', 'nagata>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'miller',
    'version': '0.1.5',
    'description': 'introspection tools using consistent, accessible syntax',
    'long_description': '"You\'re a tool that goes places. I\'m a tool that finds things." - Detective Josephus Miller\n\nNamed after the erstwhile inspector from The Expanse, this package provides \nconvenient introspection tools for packages, modules, classes, objects, \nattributes, and containers.\n\nmiller is highly internally documented so that users and developers can easily make amos work with their projects. It is designed for Python coders at all levels. Beginners should be able to follow the readable code and internal documentation to understand how it works. More advanced users should find complex and tricky problems addressed through efficient code.',
    'author': 'Corey Rayburn Yung',
    'author_email': 'coreyrayburnyung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/WithPrecedent/miller',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

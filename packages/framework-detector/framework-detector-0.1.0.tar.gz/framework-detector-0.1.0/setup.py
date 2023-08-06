# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['framework_detector',
 'framework_detector.dockerfiles',
 'framework_detector.frameworks']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.7b0,<22.0',
 'flake8>=3.9.2,<4.0.0',
 'mypy>=0.910,<0.911',
 'pre-commit>=2.14.0,<3.0.0',
 'pytest>=6.2.4,<7.0.0']

setup_kwargs = {
    'name': 'framework-detector',
    'version': '0.1.0',
    'description': 'Detects which framework is in use in a project',
    'long_description': None,
    'author': 'Miles Budden',
    'author_email': 'git@miles.so',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

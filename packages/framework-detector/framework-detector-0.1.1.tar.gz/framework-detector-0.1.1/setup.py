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
    'version': '0.1.1',
    'description': 'Detects which framework is in use in a project',
    'long_description': '# Framework detector\n\nDetects which framework is in use for a project and suggests a dockerfile.\n\nStrongly influenced by https://github.com/netlify/framework-info\n\n## Installation\n\n```sh\npip install framework-detector --extra-index-url https://__token__:<your_personal_token>@git.cardiff.ac.uk/api/v4/projects/5484/packages/pypi/simple\n```\n\n## Usage\n\n```python\nfrom framework_detector import detector, get_dockerfile\nfrom pathlib import Path\n\nframework = detector.detect(Path.cwd())\n\ndockerfile = get_dockerfile(framework["dockerfile"])\n```',
    'author': 'Miles Budden',
    'author_email': 'git@miles.so',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pbexe/framework-detector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

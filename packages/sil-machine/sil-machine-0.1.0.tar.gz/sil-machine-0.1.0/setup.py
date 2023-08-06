# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['machine',
 'machine.annotations',
 'machine.corpora',
 'machine.scripture',
 'machine.tokenization',
 'machine.utils']

package_data = \
{'': ['*']}

install_requires = \
['regex>=2021.7.6,<2022.0.0']

setup_kwargs = {
    'name': 'sil-machine',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Machine for Python\n\nMachine is a natural language processing library. It is specifically focused on providing tools and techniques that are useful for processing languages that are very resource-poor. The library is also useful as a foundation for building more advanced language processing techniques. The library currently only provides a basic set of algorithms, but the goal is to include many more in the future.\n\n## Installation\n\n```\npip install sil-machine\n```\n',
    'author': 'SIL International',
    'author_email': None,
    'maintainer': 'Damien Daspit',
    'maintainer_email': 'damien_daspit@sil.org',
    'url': 'https://github.com/sillsdev/machine.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

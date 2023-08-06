# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyass']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyass',
    'version': '0.1.0',
    'description': 'A library to read, manipulate, and write Advanced SubStation Alpha (.ass) files',
    'long_description': '# pyass\n\nA library to read, manipulate, and write Advanced SubStation Alpha (.ass) files\n',
    'author': 'xIceArcher',
    'author_email': 'xicearcher@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xIceArcher/pyass',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyzehndercloud']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<3.9.0', 'msal>=1.18.0,<1.19.0']

setup_kwargs = {
    'name': 'pyzehndercloud',
    'version': '0.1',
    'description': '',
    'long_description': '# pyZehnderCloud\n\n`pyzehndercloud` is a Python 3 library to connect to the Zehnder Cloud portal. This project is related to [pycomfoconnect](https://github.com/michaelarnauts/comfoconnect).\n\n## Usage\n\nSee `example.py` and `example_authenticate.py` for usage examples. \n\nYou first need to run `example_authenticate.py` to obtain a token, then you can use `example.py` to connect to the portal.',
    'author': 'Michaël Arnauts',
    'author_email': 'michael.arnauts@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlt645']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-dlt645',
    'version': '0.1.2',
    'description': 'A basic DL/T645-2007 communication implementation',
    'long_description': '#################################################################\npython-dlt645 - A basic DL/T645-2007 communication implementation\n#################################################################\n\nAn incomplete implementation of the DL/T645 protocol designed to communicate\nwith energy meters through an infrared interface.\n\nDevelopment\n===========\n\nWhen cloning the repository for the first time:\n\n.. code-block:: shell\n\n    $ poetry install\n    $ pre-commit install\n\nTests pre commit\n----------------\n\n.. code-block:: shell\n\n    $ black --diff dlt645/\n    $ flake8 dlt645/\n',
    'author': "Stefan 'hr' Berder",
    'author_email': 'stefan@measureofquality.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlt645']

package_data = \
{'': ['*']}

extras_require = \
{'cli': ['pyserial>=3.5,<4.0']}

entry_points = \
{'console_scripts': ['dlt645_getaddr = dlt645.cli:getaddr']}

setup_kwargs = {
    'name': 'python-dlt645',
    'version': '0.1.3',
    'description': 'A basic DL/T645-2007 communication implementation',
    'long_description': '#################################################################\npython-dlt645 - A basic DL/T645-2007 communication implementation\n#################################################################\n\nAn incomplete implementation of the DL/T645 protocol designed to communicate\nwith energy meters through an infrared interface.\n\nGetting started\n===============\n\nTo isntall the DL/T645 package only:\n\n.. code-block:: shell\n\n    $ pip install python-dlt645\n\nTo install the package with the utility CLI commands:\n\n.. code-block:: shell\n\n    $ pip install python-dlt645[cli]\n\nDevelopment\n===========\n\nWhen cloning the repository for the first time:\n\n.. code-block:: shell\n\n    $ poetry install\n    $ pre-commit install\n\nTests pre commit\n----------------\n\n.. code-block:: shell\n\n    $ black --diff dlt645/\n    $ flake8 dlt645/\n\nDocumentation\n=============\n\nBuild the documentation:\n\n.. code-block:: shell\n\n    $ make docs\n',
    'author': "Stefan 'hr' Berder",
    'author_email': 'stefan@measureofquality.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gams/python-dlt645',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

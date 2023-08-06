# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plank', 'plank.logger']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'plank-tool-logger',
    'version': '0.1.0',
    'description': 'The logger tool of plank project.',
    'long_description': 'None',
    'author': 'Grady Zhuo',
    'author_email': 'grady@ospark.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

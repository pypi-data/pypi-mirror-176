# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olympipe', 'olympipe.pipes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'olympipe',
    'version': '0.1.1',
    'description': '',
    'long_description': 'None',
    'author': 'Gabriel Kasser',
    'author_email': 'gabriel.kasser@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

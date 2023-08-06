# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['insee_number_translator', 'insee_number_translator.data']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['insee = insee_number_translator.main:main']}

setup_kwargs = {
    'name': 'insee-number-translator',
    'version': '0.2.0',
    'description': 'Translate french INSEE number to meaningful data',
    'long_description': None,
    'author': 'Gabriel Augendre',
    'author_email': 'gabriel@augendre.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

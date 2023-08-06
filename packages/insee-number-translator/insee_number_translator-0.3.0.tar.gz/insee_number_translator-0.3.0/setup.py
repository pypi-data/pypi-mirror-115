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
    'version': '0.3.0',
    'description': 'Translate french INSEE number to meaningful data',
    'long_description': '# INSEE number translator\n\nExtract data from INSEE number (France)\n\n## Getting started\n\n```shell\npyenv virtualenv 3.9.6 insee\npyenv local insee\npoetry install\n# restart your shell\ninsee 269059913116714 168127982980507\n```\n\n## Data sources\n\n- cities : https://public.opendatasoft.com/explore/dataset/correspondance-code-insee-code-postal/export/\n- countries : https://www.insee.fr/fr/information/2028273\n- departments : https://www.data.gouv.fr/fr/datasets/regions-departements-villes-et-villages-de-france-et-doutre-mer/\n',
    'author': 'Gabriel Augendre',
    'author_email': 'gabriel@augendre.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.augendre.info/gaugendre/insee_number_translator',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

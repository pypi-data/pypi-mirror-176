# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apis_ampel', 'apis_ampel.migrations']

package_data = \
{'': ['*'], 'apis_ampel': ['templates/ampel/*']}

setup_kwargs = {
    'name': 'apis-ampel',
    'version': '0.2.0',
    'description': 'Django-App for the APIS plattform. Adds status indicators to all entities that are displayed as traffic lights in list, detail and edit views.',
    'long_description': None,
    'author': 'Gregor Pirgie',
    'author_email': 'gregor.pirgie@oeaw.ac.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)

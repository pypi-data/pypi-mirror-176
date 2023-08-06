# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apis_ampel', 'apis_ampel.migrations']

package_data = \
{'': ['*'], 'apis_ampel': ['templates/ampel/*']}

install_requires = \
['Django==3.2.0',
 'PyYAML>=5.3.1,<6.0.0',
 'SPARQLWrapper>=1.8.5,<2.0.0',
 'acdh-django-charts>=0.5.3,<0.6.0',
 'convertdate>=2.3.0,<3.0.0',
 'dj-database-url>=0.5.0,<0.6.0',
 'django-admin-csvexport>=1.9,<2.0',
 'django-allow-cidr>=0.3.1,<0.4.0',
 'django-autocomplete-light>=3.9.4,<4.0.0',
 'django-cors-headers>=3.13.0,<4.0.0',
 'django-crispy-forms>=1.14.0,<2.0.0',
 'django-crum>=0.7.9,<0.8.0',
 'django-csp>=3.7,<4.0',
 'django-extensions>=3.1.3,<4.0.0',
 'django-filter>=22.1,<23.0',
 'django-guardian>=2.3.0,<3.0.0',
 'django-leaflet>=0.27.1,<0.28.0',
 'django-model-utils>=4.1.1,<5.0.0',
 'django-reversion==3.0.8',
 'django-summernote>=0.8.11,<0.9.0',
 'django-tables2>=2.4.1,<3.0.0',
 'djangorestframework-csv>=2.1.0,<3.0.0',
 'djangorestframework-jsonschema>=0.1.1,<0.2.0',
 'djangorestframework-xml>=2.0.0,<3.0.0',
 'djangorestframework==3.12.2',
 'drf-spectacular>=0.22.0,<0.23.0',
 'gunicorn>=20.0.4,<21.0.0',
 'jmespath>=0.10.0,<0.11.0',
 'jsonschema>=3.2.0,<4.0.0',
 'lxml>=4.6.2,<5.0.0',
 'mysqlclient>=2.0.3,<3.0.0',
 'numpy==1.22',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas==1.1.5',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'rdflib>=6.1.1,<6.2.0',
 'regex>=2020.11.13,<2021.0.0',
 'requests>=2.25.0,<3.0.0',
 'sentry-sdk>=1.5.12,<1.6.0',
 'tablib>=3.0.0,<4.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'typesense>=0.14.0,<0.15.0',
 'unicodecsv>=0.14.1,<0.15.0',
 'whitenoise>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'apis-ampel',
    'version': '0.1.0',
    'description': 'Django-App for the APIS plattform. Adds status indicators to all entities that are displayed as traffic lights in list, detail and edit views.',
    'long_description': None,
    'author': 'Gregor Pirgie',
    'author_email': 'gregor.pirgie@oeaw.ac.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)

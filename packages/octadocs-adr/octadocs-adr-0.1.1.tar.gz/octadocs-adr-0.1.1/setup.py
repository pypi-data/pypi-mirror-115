# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octadocs_adr', 'octadocs_adr.facets']

package_data = \
{'': ['*'], 'octadocs_adr': ['templates/octadocs-decisions/*', 'yaml/*']}

install_requires = \
['dominate>=2.6.0,<3.0.0']

entry_points = \
{'mkdocs.plugins': ['octadocs_adr = octadocs_adr.plugin:ADRPlugin']}

setup_kwargs = {
    'name': 'octadocs-adr',
    'version': '0.1.1',
    'description': 'A blueprint for Architecture Decision Record in Octadocs - the smart documentation environment.',
    'long_description': None,
    'author': 'Anatoly Scherbakov',
    'author_email': 'talk@yeti.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['housenomics',
 'housenomics.application',
 'housenomics.application.cli',
 'housenomics.application.webapi',
 'housenomics.gateways',
 'housenomics.lib',
 'housenomics.repositories']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.85,<0.86',
 'pendulum>=2.1,<2.2',
 'rich>=12.6,<12.7',
 'sqlmodel>=0.0,<0.1',
 'typer>=0.6,<0.7']

entry_points = \
{'console_scripts': ['housenomics = housenomics.application.cli.main:app']}

setup_kwargs = {
    'name': 'housenomics',
    'version': '0.0.1',
    'description': 'Manage your personal finances',
    'long_description': 'None',
    'author': 'Luís Miranda',
    'author_email': 'luistm@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)

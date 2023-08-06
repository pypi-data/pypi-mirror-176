# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snmpsim_control_plane',
 'snmpsim_control_plane.commands',
 'snmpsim_control_plane.management',
 'snmpsim_control_plane.management.exporters',
 'snmpsim_control_plane.metrics',
 'snmpsim_control_plane.metrics.importers',
 'snmpsim_control_plane.supervisor',
 'snmpsim_control_plane.supervisor.reporting',
 'snmpsim_control_plane.supervisor.reporting.formats',
 'snmpsim_control_plane.wsgi']

package_data = \
{'': ['*'], 'snmpsim_control_plane.management.exporters': ['templates/*']}

install_requires = \
['Flask-SQLAlchemy<=2.4.1',
 'Flask<=1.1.1',
 'flask-marshmallow<=0.9.0',
 'marshmallow-sqlalchemy<=0.18.0',
 'marshmallow<=2.20.5',
 'psutil']

entry_points = \
{'console_scripts': ['snmpsim-metrics-importer = '
                     'snmpsim_control_plane.commands.importer:main',
                     'snmpsim-metrics-restapi = '
                     'snmpsim_control_plane.commands.metrics:main',
                     'snmpsim-mgmt-restapi = '
                     'snmpsim_control_plane.commands.management:main',
                     'snmpsim-mgmt-supervisor = '
                     'snmpsim_control_plane.commands.supervisor:main']}

setup_kwargs = {
    'name': 'snmpsim-control-plane-lextudio',
    'version': '0.0.3',
    'description': 'REST API driven management and monitoring supervisor to remotely operate SNMP simulator.',
    'long_description': '\nSNMP Simulator Control Plane\n----------------------------\n[![PyPI](https://img.shields.io/pypi/v/snmpsim-control-plane.svg?maxAge=2592000)](https://pypi.org/project/snmpsim-control-plane/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/snmpsim-control-plane.svg)](https://pypi.org/project/snmpsim-control-plane/)\n[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/lextudio/snmpsim-control-plane/master/LICENSE.txt)\n\nSNMP Simulator Control Plane is a set of tools facilitating\nautomated, distributed and remotely controlled\n[SNMP Simulator](https://www.pysnmp.com/snmpsim) deployment.\n\nFeatures\n--------\n\n* Facilitates distributed SNMP Simulator deployment\n* Groups simulated SNMP agents into virtual labs\n* Makes SNMP simulator remotely controllable\n* Collects and serves performance and operational metrics\n* REST API is compliant to OpenAPI 3.0.0\n\nDocs & Downloads\n----------------\n\nSNMP Simulator Control Plane tool is freely available for download from\n[PyPI](https://pypi.org/project/snmpsim-control-plane/) or\n[GitHub](https://github.com/lextudio/snmpsim-control-plane/archive/master.zip).\n\nUser documentation is maintained at [pysnmp.com](https://www.pysnmp.com/snmpsim-control-plane).\n\nGetting help\n------------\n\nIf something does not work as expected,\n[open an issue](https://github.com/lextudio/pysnmp/issues) at GitHub or\npost your question [on Stack Overflow](https://stackoverflow.com/questions/ask).\n\nEveryone is welcome to fork the repo and propose a feature or a fix!\n\n\nCopyright (c) 2019-2020, [Ilya Etingof](mailto:etingof@gmail.com).\nCopyright (c) 2022, [LeXtudio Inc.](mailto:support@lextudio.com).\nAll rights reserved.\n',
    'author': 'Lex Li',
    'author_email': 'support@lextudio.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lextudio/snmpsim-control-plane',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

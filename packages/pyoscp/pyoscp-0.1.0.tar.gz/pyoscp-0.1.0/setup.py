# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oscp']

package_data = \
{'': ['*']}

install_requires = \
['flask-restx>=1.0.3,<2.0.0',
 'flask>=2.2.2,<3.0.0',
 'packaging>=21.3,<22.0',
 'requests>=2.28.1,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.0.0']}

setup_kwargs = {
    'name': 'pyoscp',
    'version': '0.1.0',
    'description': 'Python library for the Open Smart Charging Protocol (OSCP)',
    'long_description': '# pyOSCP\n\nPython Rest-Interface for Open Smart Charging Protocol (OSCP) 2.0 built on Flask-RESTX, providing a OpenAPI interface.\n\nOSCP is not as widely used as OCPI or OCPP which are much more a business standard.\nIt can be used to communicate flexibilities and capacities, having a typical negotiation process.\n\nAs version 1.x used a SOAP Approach, this can still be seen from the protocol.\nThe Registration between the participants uses a handshake and needs to have an open port on both sides.\n\nTo reduce reimplementation, an academic implementation is provided here, which furthermore allows to integrate with a new RESERVATIONS endpoint, if needed.\n\nCurrently, is no other public Python Implementation for the OSCProtocol.\nThe documentation of the protocol can be found here (https://www.openchargealliance.org/protocols/oscp-20/ - requires mail-registration)\n\n## Install Instructions\n\n`pip install pyoscp`\n\nor after cloning the repository, one can run `pip install -e .` to work locally with the package.\n\n## Package information\n\n```\noscp\n├── __init__.py\n├── *_endpoints.py      # <- contains REST Endpoint Descriptions\n├── json_models.py      # <- contains JSON Schemas in Flask-RestX\n└── RegistrationManager # <- contains stubs which have to be inherited and implemented\n```\n\n## Configuration\n\n`main.py` contains an example of how to use this project.\nThe managers are meant to be understood as interfaces, which must be implemented according to the business logic which is not part of this communications module.\n\nAn example architecture would use a background job to schedule answers (for example for the commands module) while saving the data from the post/patch requests in a seperate database, which is used for communication between the background job and the Flask app.',
    'author': 'Florian Maurer',
    'author_email': 'maurer@fh-aachen.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NOWUM/pyoscp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

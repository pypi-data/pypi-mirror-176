# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ocpi', 'ocpi.models', 'ocpi.namespaces']

package_data = \
{'': ['*']}

install_requires = \
['flask', 'flask-restx>=0.5.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.0.0']}

setup_kwargs = {
    'name': 'python-ocpi',
    'version': '0.3.1',
    'description': 'Python library for the Open Charge Point Interface (OCPI)',
    'long_description': '# pyOCPI\n\nPython Rest-Interface for OCPI (2.2) built on Flask-RESTX, providing a OpenAPI interface.\n\nTalking about OCPI, many Charge Point Operators (CPO) and e-Mobility Service Providers (eMSP) implement their own code to integrate OCPI into their software.\nThis is a very tedious way, as the protocol is very complex it is not needed that every entity implements it on their own.\n\nTo reduce reimplementation, an academic implementation is provided here, which furthermore allows to integrate with a new RESERVATIONS endpoint, if needed.\n\nCurrently, the only other public Python Implementation can be found here:\nhttps://github.com/TECHS-Technological-Solutions/ocpi/\n\nThe Documentation of OCPI can be found here:\nhttps://github.com/ocpi/ocpi/\n\n## Install Instructions\n\n`pip install pyocpi`\n\nor after cloning the repository, one can run `pip install -e .` to work locally with the package.\n\n## Package information\n\n```\npyocpi\n├── exceptions.py\n├── __init__.py\n├── managers.py # <- contains stubs which have to be inherited and implemented\n├── models      # <- contains JSON Schemas in Flask-RestX\n└── namespaces  # <- contains REST Endpoint Descriptions\n```\n\n## Configuration\n\n`main.py` contains an example of how to use this project.\nThe managers are meant to be understood as interfaces, which must be implemented according to the business logic which is not part of this communications module.\n\nAn example architecture would use a background job to schedule answers (for example for the commands module) while saving the data from the post/patch requests in a seperate database, which is used for communication between the background job and the Flask app.\n\n## Roadmap\n\nThis will not be the last iteration of this concept.\nI think this could be a lot more user friendly and abstracted, so that the usage feels more like the communication of the ocpp python package, which does not need any knowledge of the underlying websockets at all.\nYet it is a good approach and is already greatly configurable.\n\n',
    'author': 'Florian Maurer',
    'author_email': 'maurer@fh-aachen.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NOWUM/pyocpi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snmpresponder', 'snmpresponder.plugins']

package_data = \
{'': ['*']}

install_requires = \
['pysnmp-lextudio>=5.0.0']

entry_points = \
{'console_scripts': ['snmpdresponderd = snmpresponder.snmpresponderd:main']}

setup_kwargs = {
    'name': 'snmpresponder-lextudio',
    'version': '0.0.3',
    'description': 'The SNMP Command Responder application is designed to serve user data over SNMPv1/v2c/v3.',
    'long_description': '\nSNMP Command Responder\n----------------------\n\n[![PyPI](https://img.shields.io/pypi/v/snmpresponder.svg?maxAge=2592000)](https://pypi.org/project/snmpresponder)\n[![Python Versions](https://img.shields.io/pypi/pyversions/snmpresponder.svg)](https://pypi.org/project/snmpresponder/)\n[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/lextudio/snmpresponder/master/LICENSE.txt)\n\nThe SNMP Command Responder daemon runs one or more SNMP agents and maintains\none or more trees of SNMP managed objects (i.e. MIBs). The user can interface\nthose managed objects with the data they are willing to serve over SNMP.\n\nSNMP requests received by any of the embedded SNMP agents can be routed to\nany of the MIB trees for processing via a declarative mini-language.\n\nThe use-case for SNMP Command Responder is to serve user data over\nSNMP.\n\nFeatures\n--------\n\n* SNMPv1/v2c/v3 operations with built-in protocol and transport translation capabilities\n* SNMPv3 USM supports MD5/SHA/SHA224/SHA256/SHA384/SHA512 auth and\n  DES/3DES/AES128/AES192/AES256 privacy crypto algorithms\n* Maintains multiple independent SNMP engines, network transports and MIB trees\n* Discovers `pip`-installable MIB implementations\n* Extension modules supporting SNMP PDU filtering and on-the-fly modification\n* Works on Linux, Windows and OS X\n\nDownload & Install\n------------------\n\nSNMP Command Responder software is freely available for download from\n[PyPI](https://pypi.org/project/snmpresponder).\n\nJust run:\n\n```bash\n$ pip install snmpresponder-lextudio\n```\n\nAlternatively, you can get it from [GitHub](https://github.com/lextudio/snmpresponder/releases).\n\nHow to use SNMP Command Responder\n---------------------------------\n\nFirst you need to configure the tool. It is largely driven by\n[configuration files](https://www.pysnmp.com/snmpresponder/configuration/index.html)\nwritten in a declarative mini-language. To help you started, we maintain\n[a collection](https://www.pysnmp.com/snmpresponder/configuration/index.html#examples)\nof configuration files designed to serve specific use-cases.\n\nGetting help\n------------\n\nIf something does not work as expected or we are missing an interesting feature,\n[open an issue](https://github.com/lextudio/pysnmp/issues) at GitHub or\npost your question [on Stack Overflow](https://stackoverflow.com/questions/ask).\n\nFinally, your PRs are warmly welcome! ;-)\n\nCopyright (c) 2019, [Ilya Etingof](mailto:etingof@gmail.com).\nCopyright (c) 2022, [LeXtudio Inc.](mailto:support@lextudio.com).\nAll rights reserved.\n',
    'author': 'Lex Li',
    'author_email': 'support@lextudio.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lextudio/snmpresponder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

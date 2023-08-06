# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snmpfwd', 'snmpfwd.plugins', 'snmpfwd.scripts', 'snmpfwd.trunking']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodomex>=3.11.0,<4.0.0', 'pysnmp-lextudio>=4.4.3']

entry_points = \
{'console_scripts': ['snmpfwd-client = snmpfwd.scripts.snmpfwdclient:main',
                     'snmpfwd-server = snmpfwd.scripts.snmpfwdserver:main']}

setup_kwargs = {
    'name': 'snmpfwd-lextudio',
    'version': '0.4.4',
    'description': 'SNMP Proxy Forwarder can act as an application-level firewall or SNMP protocol translator that let SNMPv1/v2c entities to talk to SNMPv3 ones or vice-versa.',
    'long_description': '\nSNMP Proxy Forwarder\n--------------------\n\n[![PyPI](https://img.shields.io/pypi/v/snmpfwd.svg?maxAge=2592000)](https://pypi.org/project/snmpfwd)\n[![Python Versions](https://img.shields.io/pypi/pyversions/snmpfwd.svg)](https://pypi.org/project/snmpfwd/)\n[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/lextudio/snmpfwd/master/LICENSE.txt)\n\nThe SNMP Proxy Forwarder tool works as an application-level proxy with a built-in\nSNMP message router. SNMP forwarder design features split client/server operation\nthat promotes having one part of the system in DMZ while other part is \nfacing the Internet. Message routing can be programmed via a declarative\nmini-language.\n\nTypical use case for an SNMP proxy is to work as an application-level firewall\nor a protocol translator that enables SNMPv3 access to a SNMPv1/SNMPv2c\nentity or vice versa.\n\nFeatures\n--------\n\n* SNMPv1/v2c/v3 operations with built-in protocol and transport translation capabilities\n* SNMPv3 USM supports MD5/SHA/SHA224/SHA256/SHA384/SHA512 auth and\n  DES/3DES/AES128/AES192/AES256 privacy crypto algorithms\n* Forwards SNMP commands and notifications\n* Maintains multiple independent SNMP engines and network transports\n* Split client and server parts interconnected through encrypted TCP links\n* Flexible SNMP PDU routing\n* Extension modules supporting SNMP PDU filtering and on-the-fly modification\n* Supports transparent proxy operation (Linux only)\n* Works on Linux, Windows and OS X\n\nDownload & Install\n------------------\n\nSNMP Proxy Forwarder software is freely available for download from\n[PyPI](https://pypi.org/project/snmpfwd).\n\nJust run:\n\n```bash\n$ pip install snmpfwd-lextudio\n```\n\nAlternatively, you can get it from [GitHub](https://github.com/lextudio/snmpfwd/releases).\n\nHow to use SNMP proxy forwarder\n-------------------------------\n\nFirst you need to configure the tool. It is largely driven by\n[configuration files](https://www.pysnmp.com/snmpfwd/configuration/index.html)\nwritten in a declarative mini-language. To help you started, we maintain\n[a collection](https://www.pysnmp.com/snmpfwd/configuration/index.html#examples)\nof configuration files designed to serve specific use-cases.\n\nGetting help\n------------\n\nIf something does not work as expected or we are missing an interesting feature,\n[open an issue](https://github.com/lextudio/pysnmp/issues) at GitHub or\npost your question [on Stack Overflow](https://stackoverflow.com/questions/ask).\n\nFinally, your PRs are warmly welcome! ;-)\n\nCopyright (c) 2014-2019, [Ilya Etingof](mailto:etingof@gmail.com).\nCopyright (c) 2022, [LeXtudio Inc.](mailto:support@lextudio.com).\nAll rights reserved.\n',
    'author': 'Lex Li',
    'author_email': 'support@lextudio.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lextudio/snmpfwd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

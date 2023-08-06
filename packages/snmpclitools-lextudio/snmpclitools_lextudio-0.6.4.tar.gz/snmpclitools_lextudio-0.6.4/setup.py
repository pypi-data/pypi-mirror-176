# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snmpclitools', 'snmpclitools.cli', 'snmpclitools.scripts']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodomex>=3.11.0,<4.0.0',
 'pysmi-lextudio>=0.3.4',
 'pysnmp-lextudio>=4.4.4']

entry_points = \
{'console_scripts': ['snmpbulkwalk = snmpclitools.scripts.snmpbulkwalk:start',
                     'snmpget = snmpclitools.scripts.snmpget:start',
                     'snmpset = snmpclitools.scripts.snmpset:start',
                     'snmptranslate = snmpclitools.scripts.snmptranslate:start',
                     'snmptrap = snmpclitools.scripts.snmptrap:start',
                     'snmpwalk = snmpclitools.scripts.snmpwalk:start']}

setup_kwargs = {
    'name': 'snmpclitools-lextudio',
    'version': '0.6.4',
    'description': 'A collection of command-line tools for SNMP management purposes built on top of PySNMP package.',
    'long_description': '\nCommand-line SNMP tools\n-----------------------\n\n[![PyPI](https://img.shields.io/pypi/v/snmpclitools.svg?maxAge=2592000)](https://pypi.org/project/snmpclitools)\n[![Python Versions](https://img.shields.io/pypi/pyversions/snmpclitools.svg)](https://pypi.org/project/snmpclitools/)\n[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/pysnmp/snmpclitools/master/LICENSE.rst)\n\nThis is a collection of command-line SNMP tools written in pure-Python.\nThe tools mimic their famous [Net-SNMP](https://sourceforge.net/projects/net-snmp/)\ncounterparts.\n\nIn the past this project was known as *pysnmp-apps*.\n\nFeatures\n--------\n\n* Complete SNMPv1/v2c and SNMPv3 support\n* Interface compatible (almost) with Net-SNMP\'s snmp\\* tools.\n* SNMPv3 USM supports MD5/SHA/SHA224/SHA256/SHA384/SHA512 auth and\n  DES/3DES/AES128/AES192/AES256 privacy crypto algorithms\n* Automatically downloads required MIBs from the Internet\n* Runs over IPv4 and/or IPv6 transports\n* Cross-platform: works on Linux, Windows and OS X.\n* 100% Python, works with Python 2.4 up to Python 3.7\n\nDownload\n--------\n\nThe snmpclitools package is distributed under terms and conditions of 2-clause\nBSD [license](https://www.pysnmp.com/snmpclitools/license.html). Source code is freely\navailable as a Github [repo](https://github.com/lextudio/snmpclitools).\n\nInstallation\n------------\n\nDownload snmpclitools from [PyPI](https://pypi.org/project/snmpclitools) or just run:\n\n```bash\n$ pip install snmpclitools-lextudio\n```\n\nHow to use the tools\n--------------------\n\nThe most of pysnmp command-line tools could be run in a similar way as \ntheir Net-SNMP counterparts. For example:\n\n```bash\n$ snmpbulkwalk.py -v3 -u usr-md5-des -l authPriv -A authkey1 -X privkey1 demo.pysnmp.com system\nSNMPv2-MIB::sysDescr.0 = DisplayString: Linux grommit 3.5.11.1 #2 PREEMPT Tue Mar 1 14:03:24 MSD 2016 i686 unknown unknown GNU/Linux\nSNMPv2-MIB::sysObjectID.0 = ObjectIdentifier: iso.org.dod.internet.private.enterprises.8072.3.2.101.3.6.1.4.1.8072.3.2.10\nSNMPv2-MIB::sysUpTime.0 = TimeTicks: 43 days 1:55:47.85372214785\n[ skipped ]\nSNMPv2-MIB::sysORUpTime."8" = TimeStamp: 0 days 0:0:0.77\nSNMPv2-MIB::sysORUpTime."9" = TimeStamp: 0 days 0:0:0.77\n\n$ snmpget.py -v3 -u usr-sha-aes -l authPriv -A authkey1 -X privkey1 demo.pysnmp.com IP-MIB::ipAdEntBcastAddr.\\"127.0.0.1\\"\nIP-MIB::ipAdEntBcastAddr."127.0.0.1" = Integer32: 1\n\n$ snmpset.py -v2c -c public demo.pysnmp.com SNMPv2-MIB::sysDescr.0 = my-new-descr\nnotWritable(17)\n```\n\nFor more information, please, run any of these tools with `--help` option.\n\nYou can play with different security protocols against the publicly available SNMP\nagent like [this one @www.pysnmp.com](https://www.pysnmp.com/snmpsim/public-snmp-agent-simulator.html).\n\nGetting help\n------------\n\nIf something does not work as expected, please open up a\n[GitHub issue](https://github.com/lextudio/pysnmp/issues/new) or post\nyour question [to Stack Overflow](https://stackoverflow.com/questions/ask).\n\nFeedback and collaboration\n--------------------------\n\nI\'m interested in bug reports, fixes, suggestions and improvements. Your\npull requests are very welcome!\n\nCopyright (c) 2005-2019, [Ilya Etingof](mailto:etingof@gmail.com).\nCopyright (c) 2022, [LeXtudio Inc.](mailto:support@lextudio.com).\nAll rights reserved.\n\n',
    'author': 'Lex Li',
    'author_email': 'support@lextudio.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lextudio/snmpclitools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

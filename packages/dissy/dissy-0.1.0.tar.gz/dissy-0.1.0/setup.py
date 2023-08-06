# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dissy', 'dissy.disassemblers']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.6.0,<13.0.0', 'textual>=0.4.0,<0.5.0']

extras_require = \
{'x64': ['distorm3>=3.5.2,<4.0.0']}

entry_points = \
{'console_scripts': ['dissy = dissy.app:main']}

setup_kwargs = {
    'name': 'dissy',
    'version': '0.1.0',
    'description': 'An interactive disassembler console UI',
    'long_description': None,
    'author': 'Anthony Shaw',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

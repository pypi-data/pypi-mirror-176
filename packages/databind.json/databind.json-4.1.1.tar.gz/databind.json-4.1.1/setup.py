# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['json']

package_data = \
{'': ['*']}

install_requires = \
['databind.core>=4.1.1,<5.0.0',
 'nr-date>=2.0.0,<3.0.0',
 'typeapi>=1.2.1,<2.0.0',
 'typing-extensions>=3.10.0']

setup_kwargs = {
    'name': 'databind.json',
    'version': '4.1.1',
    'description': 'De-/serialize Python dataclasses to or from JSON payloads. Compatible with Python 3.7 and newer.',
    'long_description': '# databind.json\n\nThe `databind.json` package implements the de-/serialization to or from JSON payloads using\nthe `databind.core` framework.\n\nCheck out the [Documentation][0] for examples.\n\n[0]: https://niklasrosenstein.github.io/python-databind/\n\n---\n\n<p align="center">Copyright &copy; 2020 &ndash; Niklas Rosenstein</p>\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.3,<4.0.0',
}


setup(**setup_kwargs)

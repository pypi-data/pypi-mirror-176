# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wica']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'py-wica',
    'version': '1.0.3',
    'description': 'A simple python API to access wica-http SSE.',
    'long_description': '# Py-Wica\n#### Table of Contents\n- [Introduction](#introduction)\n- [Installation](#installation)\n- [Quick-start Guid](#quick-start-guide)\n- [Documentation](#documentation)\n- [Dependencies](#dependencies)\n- [Contribute](#contribute)\n- [Project Changes and Tagged Releases](#project-changes-and-tagged-releases)\n- [Developer Notes](#developer-notes)\n- [Contact](#contact)\n\n# Introduction\nSimple Python API for connecting to a wica-http server and streaming data.\nSupport for blocking and non blocking operation.\n\n\n# Installation\n\n# Quick-start Guide\n\n# Documentation\n\n# Dependencies\n\n# Contribute\n\n# Project Changes and Tagged Releases\n\n# Developer Notes\n\n# Contact',
    'author': 'Niklas Laufkoetter',
    'author_email': 'niklas.laufkoetter@psi.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

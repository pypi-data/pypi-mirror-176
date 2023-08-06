# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['symnet_cp']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1.0,<23.0.0', 'prometheus-client>=0.14.1,<0.15.0']

setup_kwargs = {
    'name': 'symnet-cp',
    'version': '0.3.0',
    'description': 'SymNet External Control Protocol implementation',
    'long_description': '# SymNet Control Protocol implementation\n\n[![PyPI](https://img.shields.io/pypi/v/symnet-cp)](https://pypi.org/project/symnet-cp/)\n[![Tests](https://github.com/chrko/python-symnet-cp/actions/workflows/tests.yml/badge.svg)](https://github.com/chrko/python-symnet-cp/actions/workflows/tests.yml)\n[![codecov](https://codecov.io/gh/chrko/python-symnet-cp/branch/main/graph/badge.svg?token=hUXpLvpMJi)](https://codecov.io/gh/chrko/python-symnet-cp)\n\nThis is an asyncio implementation of the [SymNet Control Protocol](https://www.symetrix.co/repository/SymNet_cp.pdf).\nAt bermudafunk we use this to control a Solus 16x8.\n',
    'author': 'Christian Kohlstedde',
    'author_email': 'christian@kohlsted.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

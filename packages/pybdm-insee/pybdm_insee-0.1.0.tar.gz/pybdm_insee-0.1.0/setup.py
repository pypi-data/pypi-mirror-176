# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybdm_insee', 'pybdm_insee.tools', 'pybdm_insee.tools.attrdict']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'colorama>=0.4.6,<0.5.0',
 'lxml>=4.9.1,<5.0.0',
 'pandas>=1.5.1,<2.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['insee = pybdm_insee.main:cli']}

setup_kwargs = {
    'name': 'pybdm-insee',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

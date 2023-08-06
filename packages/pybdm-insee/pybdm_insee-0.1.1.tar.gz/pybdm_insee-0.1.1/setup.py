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
    'version': '0.1.1',
    'description': '',
    'long_description': '# My very first package !\n\nThis is a very simple package helping people use the [IBDM api from french INSEE](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=BDM&version=V1&provider=insee).',
    'author': "Arno's Stuff",
    'author_email': 'bcda0276@gmail.com',
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

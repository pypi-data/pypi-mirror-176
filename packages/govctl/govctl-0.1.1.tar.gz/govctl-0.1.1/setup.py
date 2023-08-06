# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['govctl']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['govctl = govctl.main:app']}

setup_kwargs = {
    'name': 'govctl',
    'version': '0.1.1',
    'description': 'GOV.PF Multifunction CLI',
    'long_description': '',
    'author': 'Leonard TAVAE',
    'author_email': 'leonard.tavae@gmail.com',
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

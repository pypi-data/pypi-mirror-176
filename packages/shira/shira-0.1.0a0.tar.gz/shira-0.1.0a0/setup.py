# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shira']

package_data = \
{'': ['*']}

install_requires = \
['textual[dev]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['shira = shira.shira:run']}

setup_kwargs = {
    'name': 'shira',
    'version': '0.1.0a0',
    'description': 'Investigate!',
    'long_description': '',
    'author': 'Darren Burns',
    'author_email': 'darrenb900@gmail.com',
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

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['guarana', 'guarana.schemas', 'guarana.trackers']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'pydantic>=1.10.2,<2.0.0',
 'segment-analytics-python>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'guarana',
    'version': '2.4.3',
    'description': '',
    'long_description': 'None',
    'author': 'Rodrigo Godinho',
    'author_email': 'rodrigolegod@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['musamusa_fal']

package_data = \
{'': ['*']}

install_requires = \
['iaswn>=0.0.6,<0.0.7', 'rich>=10.2.0,<11.0.0']

setup_kwargs = {
    'name': 'musamusa-fal',
    'version': '0.1.4',
    'description': 'Use this package to store a filename and a line number.',
    'long_description': None,
    'author': 'suizokukan',
    'author_email': 'suizokukan@orange.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

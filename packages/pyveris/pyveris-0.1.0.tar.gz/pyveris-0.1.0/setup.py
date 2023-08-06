# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyveris']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'pyveris',
    'version': '0.1.0',
    'description': 'Converis API client written in python',
    'long_description': '# pyveris\n\n[Converis](https://clarivate.com/webofsciencegroup/solutions/converis/) API client written in python.\n',
    'author': 'André Sartori',
    'author_email': 'sartori@ebi.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

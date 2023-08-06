# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rttlib']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'rttlib',
    'version': '0.1.0',
    'description': 'Wrapper for the RealTimeTrains API',
    'long_description': '# rttlib\nWrapper for the [RealTimeTrains API](https://api.rtt.io).\n',
    'author': 'lyiriyah',
    'author_email': 'lyiriyah@tutanota.com',
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

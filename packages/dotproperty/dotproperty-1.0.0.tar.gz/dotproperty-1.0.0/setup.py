# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dotproperty']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dotproperty',
    'version': '1.0.0',
    'description': 'dotproperty',
    'long_description': '## dotproperty\n\n## Description:\n#    dotproperty\n',
    'author': 'wayfaring-stranger',
    'author_email': 'zw6p226m@duck.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchlight', 'torchlight.training']

package_data = \
{'': ['*']}

install_requires = \
['pycarton>=0.3.0,<0.4.0',
 'pytorch-ignite>=0.4.5,<0.5.0',
 'torch>=1.9.0,<2.0.0',
 'transformers>=4.8.1,<5.0.0']

setup_kwargs = {
    'name': 'pytorch-light',
    'version': '0.1.2',
    'description': 'Light.',
    'long_description': None,
    'author': 'Yevgnen Koh',
    'author_email': 'wherejoystarts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

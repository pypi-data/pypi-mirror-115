# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylark']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'pylark',
    'version': '0.0.4',
    'description': 'Feishu/Lark Open API Python Sdk, Support ALL Open API and Event Callback.',
    'long_description': None,
    'author': 'chyroc',
    'author_email': 'chyroc@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)

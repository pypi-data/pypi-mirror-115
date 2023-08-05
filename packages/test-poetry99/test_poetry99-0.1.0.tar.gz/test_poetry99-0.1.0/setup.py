# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_poetry99']

package_data = \
{'': ['*'],
 'test_poetry99': ['static/*',
                   'templates/*',
                   'templates/auth/*',
                   'templates/blog/*']}

install_requires = \
['Flask>=2.0.1,<3.0.0', 'gunicorn>=20.1.0,<21.0.0']

setup_kwargs = {
    'name': 'test-poetry99',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'yefei',
    'author_email': 'fei_ye@hxecloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

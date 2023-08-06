# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optic_django_unittest']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.4,<4.0.0',
 'kubi-ecs-logger>=0.1.0,<0.2.0',
 'optic-django-middleware>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'optic-django-unittest-plugin',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mukesh',
    'author_email': 'mmukesh95@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

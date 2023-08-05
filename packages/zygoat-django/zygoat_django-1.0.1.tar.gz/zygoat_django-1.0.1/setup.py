# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zygoat_django',
 'zygoat_django.management',
 'zygoat_django.management.commands',
 'zygoat_django.middleware',
 'zygoat_django.settings']

package_data = \
{'': ['*']}

install_requires = \
['django-environ>=0.4.4',
 'django-redis>=5.0.0',
 'django>=2',
 'djangorestframework-camel-case>=1.2.0',
 'djangorestframework>=3.9.1',
 'importlib-metadata>=4.11.3,<5.0.0',
 'uvicorn[standard]>=0.13.0']

setup_kwargs = {
    'name': 'zygoat-django',
    'version': '1.0.1',
    'description': '',
    'long_description': 'None',
    'author': 'Mark Rawls',
    'author_email': 'markrawls96@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

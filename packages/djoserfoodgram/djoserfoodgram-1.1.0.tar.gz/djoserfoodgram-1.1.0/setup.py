# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djoserfoodgram',
 'djoserfoodgram.social',
 'djoserfoodgram.social.backends',
 'djoserfoodgram.social.token',
 'djoserfoodgram.urls']

package_data = \
{'': ['*'],
 'djoserfoodgram': ['locale/de/LC_MESSAGES/django.po',
            'locale/es/LC_MESSAGES/django.po',
            'locale/fr/LC_MESSAGES/django.po',
            'locale/ka/LC_MESSAGES/django.po',
            'locale/pl/LC_MESSAGES/django.po',
            'locale/pt_BR/LC_MESSAGES/django.po',
            'locale/ru_RU/LC_MESSAGES/django.po',
            'templates/email/*']}

install_requires = \
['asgiref>=3.2.10,<4.0.0',
 'coreapi>=2.3.3,<3.0.0',
 'django-templated-mail>=1.1.1,<2.0.0',
 'djangorestframework-simplejwt>=4.3.0,<5.0.0',
 'social-auth-app-django>=4.0.0,<5.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0'],
 'test': ['pytest>=6.0.2,<7.0.0',
          'codecov>=2.0.16,<3.0.0',
          'coverage>=5.3,<6.0',
          'pytest-cov>=2.10.1,<3.0.0',
          'pytest-django>=3.10.0,<4.0.0',
          'pytest-pythonpath>=0.7.3,<0.8.0',
          'djet>=0.2.2,<0.3.0']}

setup_kwargs = {
    'name': 'djoserfoodgram',
    'version': '1.1.0',
    'description': 'REST implementation of Django authentication system.',
    'author_email': 'nosov1995@gmail.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

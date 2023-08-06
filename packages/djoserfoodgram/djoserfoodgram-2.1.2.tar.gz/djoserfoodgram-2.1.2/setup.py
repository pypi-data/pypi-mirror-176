import setuptools

setuptools.setup(
	name='djoserfoodgram',
	version='2.1.2',
	author='avnosov',
	author_email='nosov1995@gmail.com',
	description='',
	packages=['djoserfoodgram',
 'djoserfoodgram.social',
 'djoserfoodgram.social.backends',
 'djoserfoodgram.social.token',
 'djoserfoodgram.urls'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
        package_data = \
{'': ['*'],
 'djoserfoodgram': ['locale/de/LC_MESSAGES/django.po',
            'locale/es/LC_MESSAGES/django.po',
            'locale/fr/LC_MESSAGES/django.po',
            'locale/ka/LC_MESSAGES/django.po',
            'locale/pl/LC_MESSAGES/django.po',
            'locale/pt_BR/LC_MESSAGES/django.po',
            'locale/ru_RU/LC_MESSAGES/django.po',
            'templates/email/*']},

	python_requires='>=3.6',
)

import setuptools

setuptools.setup(
	name='djoserfoodgram',
	version='1.2.7',
	author='avnosov',
	author_email='nosov1995@gmail.com',
	description='',
	packages=['djoser',
 'djoser.social',
 'djoser.social.backends',
 'djoser.social.token',
 'djoser.urls'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
        package_data = \
{'': ['*'],
 'djoser': ['locale/de/LC_MESSAGES/django.po',
            'locale/es/LC_MESSAGES/django.po',
            'locale/fr/LC_MESSAGES/django.po',
            'locale/ka/LC_MESSAGES/django.po',
            'locale/pl/LC_MESSAGES/django.po',
            'locale/pt_BR/LC_MESSAGES/django.po',
            'locale/ru_RU/LC_MESSAGES/django.po',
            'templates/email/*']},

	python_requires='>=3.6',
)

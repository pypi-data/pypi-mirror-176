import setuptools

setuptools.setup(
	name='djoserfoodgram',
	version='1.2.6',
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
	python_requires='>=3.6',
)

import setuptools
with open(r'C:\Users\zadvo\Desktop\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='PyQwidgets',
	version='0.2.1',
	author='Georg8528',
	author_email='zadvornow2908@gmail.com',
	description='This mini-framework will help you create a widget!',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['PyQwidgets'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)
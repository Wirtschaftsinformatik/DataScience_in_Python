# https://setuptools.readthedocs.io/en/latest/setuptools.html

from setuptools import setup, find_packages

with open("README", 'r') as f:
	long_description = f.read()

setup(
	name='FSUSetupSample',
	version='1.0.2',
	install_requires=['logging'],
	python_requires='>3.6.0',
	# external packages as dependencies
	url='https://www.wiinf.uni-jena.de',
	license='GPL 3.0',
	author='Lehrstuhl Wirtschaftsinformatik FSU Jena',
	author_email='email@uni-jena.de',
	description='Sample zur Demonstration des Setup files',
	scripts=[
		'main.py',
		'scripts/MyScript.py'
	],
	packages=find_packages(exclude=["tests", "*.tests"]),
	include_package_data=True
)
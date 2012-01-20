from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-junar',
	version=version,
	description="",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Luis Felipe \xc3\x81lvarez',
	author_email='falvarez@ciudadanointeligente.cl',
	url='',
	license='AGPL',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.junar'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	# Add plugins here, eg
	junar=ckanext.junar:Junar
	""",
)

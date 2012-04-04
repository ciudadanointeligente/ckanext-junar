import sys
import re
from pprint import pprint
import logging
from ckan.lib.cli import CkanCommand

log = logging.getLogger(__name__)


class Junar(CkanCommand):
	'''Helps with certain operations in the Junar plugin context

    Usage:
        junar initdb
            Creates the necessary tables.
      
    The commands should be run from the ckanext-junar directory and expect
    a development.ini file to be present. Most of the time you will
    specify the config explicitly though::

        paster junar initdb --config=../ckan/development.ini

    '''


	summary = __doc__.split('\n')[0]
	usage = __doc__
	max_args = 1
	min_args = 0

	def command(self):
		self._load_config()
		print ''
		if len(self.args) == 0:
			self.parser.print_usage()
			sys.exit(1)
		cmd = self.args[0]
		if cmd == 'initdb':
			self.initdb()
		else:
			print 'Command %s not recognized' % cmd

	def initdb(self):
		from ckanext.junar.model import setup
		setup()
		print 'DB tables created'

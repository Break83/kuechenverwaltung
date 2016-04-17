import os
import ConfigParser

class Parser(ConfigParser.ConfigParser):

	def __init__(self):
		ConfigParser.ConfigParser.__init__(self)
		self.read(os.path.join(os.path.dirname(__file__), 'config.ini'))



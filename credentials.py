
import ConfigParser
import unittest

class TestCredentialBase(object):
	def load_credentials(self):
		config = ConfigParser.RawConfigParser()
		config.readfp( open('credentials.conf')  )
		self.username = config.get('fimfiction','username')
		self.password = config.get('fimfiction','password')
		
if __name__ == '__main__':
	c = TestCredentialBase()
	c.load_credentials()
	print "Using username = %s", c.username

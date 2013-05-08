import unittest
import logging

import fimfictionapi
import search
import readlater

import url as URL

# @unittest.skip("Skipping authless test.")
class TestReadLaterLoggedOut(unittest.TestCase):
	def setUp(self):
		self.api = fimfictionapi.FimFictionAPI()
		self.rl = readlater.ReadLater(self.api)
		logging.basicConfig(format="%(asctime)s %(levelname)s: %(filename)s:%(lineno)d:%(funcName)s : %(message)s", level=logging.DEBUG)			
	
	def test_add_readitlater_while_logged_out(self):
		self.assertRaises( readlater.ReadLaterException, self.rl.add, 100 )
	def test_remove_readitlater_while_logged_out(self):
		self.assertRaises( readlater.ReadLaterException, self.rl.remove, 100 )
	def test_list_readitlater_while_logged_out(self):
		self.assertRaises( fimfictionapi.NotLoggedInException, self.rl.fetch )
		
class TestReadLater(unittest.TestCase, TestCredentialBase):
	def setUp(self):
		self.load_credentials()
		self.api = fimfictionapi.FimFictionAPI()
		self.api.login( self.username, self.password )
		self.rl = readlater.ReadLater(self.api)
		logging.basicConfig(format="%(asctime)s %(levelname)s: %(filename)s:%(lineno)d:%(funcName)s : %(message)s", level=logging.DEBUG)			
	
	def test_fetch_readitlater(self):
		stories = self.rl.fetch()
		self.assertGreater( len(stories), 0 )
	
	def test_add_remove(self):
		# Assumes StoryID 100 is not on the ReadLater list at the start.
		storyid = 100
		storyidstr = str(storyid)
		
		logging.info("Fetching initial list.")
		stories = self.rl.fetch()
		self.assertNotIn( storyidstr, stories )
		
		logging.info("Add & check list.")
		
		self.rl.add(storyid)
		stories = self.rl.fetch()
		self.assertIn( storyidstr, stories )
		
		logging.info("Remove & check list.")
		self.rl.remove(storyid)
		stories = self.rl.fetch()
		self.assertNotIn( storyidstr, stories )
		
		logging.info("Done.")

if __name__ == '__main__':
	print "For less detail, run tests as:  python -m unittest  discover -b -v"
	unittest.main(buffer=True)

import unittest
import logging

import fimfictionapi
import search
import markread

from credentials import *

@unittest.skip("Skipping authless test.")
class TestMarkReadLoggedOut(TestCredentialBase):
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
		
class TestMarkRead(unittest.TestCase, TestCredentialBase):
	def setUp(self):
		self.load_credentials()
		self.api = fimfictionapi.FimFictionAPI()
		self.api.login( self.username, self.password )
		self.read = markread.MarkRead(self.api)
		logging.basicConfig(format="%(asctime)s %(levelname)s: %(filename)s:%(lineno)d:%(funcName)s : %(message)s", level=logging.DEBUG)			
		
	def test_add_remove(self):
		# Assumes StoryId 100 is not on the ReadLater list at the start.
		storyid = 100
		storyidstr = str(storyid)
		
		# First chapter of StoryId 100
		chapterId = 3911
		
		self.assertTrue( self.read.mark_read(chapterId) ) 
		self.assertTrue( self.read.mark_unread(chapterId) )
		self.assertTrue( self.read.toggle(chapterId) )
		self.assertTrue( self.read.mark_unread(chapterId) )
		
if __name__ == '__main__':
	print "For less detail, run tests as:  python -m unittest  discover -b -v"
	unittest.main(buffer=True)

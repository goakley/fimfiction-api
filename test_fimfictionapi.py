import unittest
import logging

import fimfictionapi
import search
import markread

import url as URL


class TestAPILogin(unittest.TestCase):
	def setUp(self):
		self.load_credentials()
		self.api = fimfictionapi.FimFictionAPI()
	
	def test_login(self):
		self.assertTrue( self.api.login(self.username, self.password) )

class TestLoggedOutAPI(unittest.TestCase):
	def setUp(self):
		self.api = fimfictionapi.FimFictionAPI()

	def test_fetch_readitlater(self):
		url = search.SearchAPI.search_url(read_it_later=True)
		self.assertRaises( fimfictionapi.NotLoggedInException, self.api.fetch_story_list, url )
	

class TestAPI(unittest.TestCase):
	def setUp(self):
		self.load_credentials()
		self.api = fimfictionapi.FimFictionAPI()
		self.api.login( self.username, self.password)

	
	def test_fetch_readitlater(self):
		url = search.SearchAPI.search_url(read_it_later=True)
		stories = self.api.fetch_story_list(url)
		self.assertGreater( len(stories), 0 )
		
	def test_fetch_story_list(self):
		stories = self.api.fetch_story_list('http://www.fimfiction.net/index.php?compact_view=1&view=category&search=&order=heat&category_romance=1&category_tragedy=&category_sad=&category_dark=&category_comedy=&category_random=&category_crossover=&category_adventure=&category_slice_of_life=&category_alternate_universe=&category_human=&content_rating=-1&mature_categories=0&completed=1&minimum_words=&maximum_words=&characters%5B%5D=46&characters%5B%5D=47')
		self.assertGreater( len(stories), 0 )



class TestMarkRead(unittest.TestCase):
	def setUp(self):
		self.load_credentials()
		self.api = fimfictionapi.FimFictionAPI()
		self.api.login( self.username, self.password)
	
	def test_toggle(self):
		mr = markread.MarkRead(self.api)
		# Chapter 1 of http://www.fimfiction.net/story/19198/background-pony
		self.assertNotEqual( mr.toggle(58886), mr.toggle(58886) )
		
if __name__ == '__main__':
	logging.basicConfig(format="%(asctime)s %(levelname)s: %(filename)s:%(lineno)d:%(funcName)s : %(message)s", level=logging.DEBUG)

	print "For more detail, run tests as:  python -m unittest  discover -b -v"
	unittest.main(buffer=True)

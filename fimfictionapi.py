
import url as URL

from bs4 import BeautifulSoup, BeautifulStoneSoup
import urllib2
import urllib
import urlparse
import html5lib
import re
import json
from cookielib import CookieJar, Cookie
import os
import cgi

import zipfile

import xml.etree.ElementTree as ET

import logging


class NotLoggedInException(Exception):
	def __str__(self):
		return "Not authenticated."

class Search:
	opener = None
	cj = None
	

class FimFictionAPI:
	def __init__(self):
		self.cj = CookieJar()
		
	
	def set_mature(self, new):
		val = 'false'
		if(new):
			val = 'true'
		ck = Cookie(version=0, name='view_mature', value=val, port=None, port_specified=False, domain='www.fimfiction.net', domain_specified=True, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
		self.cj.set_cookie(ck)
		
	def login(self, username, password):
		url = URL.URL.LOGIN
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		formdata = {"username":username, "password":password}
		data_encoded = urllib.urlencode(formdata)
		
		response = opener.open(url, data_encoded)
		content = response.read()
		
		if( content == "0" ):
			return True
		raise NotLoggedInException()
		
	def fetch_story_list(self, url, morepages=0, require_authentication=True):
		try:
			logging.info("Fetching story list from %s" % url)
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
			
			page = opener.open(url)
			soup = BeautifulSoup(page)
			
		
			if soup.find(id='login_username'):
				logging.error("Not logged in!")
				if require_authentication:
					raise NotLoggedInException()
				
			if soup.find(id='button button_logout'):
				logging.debug("Logged in!")
			
			
			if( soup.find(class_='browse_stories').tbody == None ):
				return []
			rows = soup.find(class_='browse_stories').tbody.find_all("tr")
			
			stories = []
			
			re_story_id = re.compile("/story/([0-9]+)/")
			for row in rows:
				try:
					story_data = row.find(class_='story_data')					
					m = re_story_id.match( story_data.find(href=re_story_id)['href'] )
					if m:
						stories.append( m.group(1) )
				except:
					logging.error("Error matching in row. Skipping.")
					pass	
			# Recursively fetch list.
			if( len(stories)>0 and morepages>0 ):
				next_page_url = soup.find(class_='page_list').find("a", text=re.compile("Next Page") )['href']
				next_page_url_corrected = urlparse.urljoin( url, next_page_url )
				stories = stories + self.fetch_story_list(next_page_url_corrected, morepages-1)
			return stories
			
		except:
			print "Exception encountered while processing %s" % url
			raise
			
	def fetch_story_metadata(self, story_id):
		fp = urllib2.urlopen(URL.URL.API_BASE + story_id)
		metadata = json.load(fp)

		print metadata

		cats=[]
		for c in metadata['story']['categories']:
			if metadata['story']['categories'][c] == True:
				cats.append(c)

		cats.append( metadata['story']['content_rating_text'] )
		
		print cats
			
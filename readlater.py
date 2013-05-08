import search
import url as URL

import logging
import urllib2
import urllib
import xml.etree.ElementTree as ET


#	READLATER	= AJAX + 'add_read_it_later.php'
#	FAVOURITE	= AJAX + 'add_favourite.php'
#	READ		= AJAX + 'toggle_read.php'
#	RATE		= AJAX + 'rate.php'

class ReadLaterException(Exception):
	pass
	
class ReadLater:
	cj = None
	
	def __init__(self, api):
		self.api = api
		self.cj = api.cj
		
	def fetch(self, completed=None):
		url = search.SearchAPI.search_url(read_it_later=True, completed=completed)
		# url = 'http://www.fimfiction.net/index.php?view=category&read_it_later=1&compact_view=1'
		stories = self.api.fetch_story_list(url, 4)
		logging.debug("Fetched read later list: %d stories" % len(stories))
		return stories
	
	
	def remove(self,story):
		try:
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
			formdata = {"story":story, "selected":"0"}
			data_encoded = urllib.urlencode(formdata)
		
			response = opener.open(URL.URL.READLATER, data_encoded)
			content = response.read()
			root = ET.fromstring(content)
			logging.debug(content)
			try:
				if( root.findall("selected") == [] ):
					raise ReadLaterException()
					
				if( root.findall("selected")[0].text == "0" ):
					logging.info("Removed story %s from read-it-later list." % story)
					return True
				else:
					logging.warning("Story %s was already removed from read-it-later list." % story)
			except:
				logging.error("Failed attempting to remove story %s from read-it-later list!" % story)
				logging.debug(content)
				
		except ET.ParseError as e:
			logging.error("Failed attempting to remove story %s from read-it-later list, xml.etree.ElementTree.ParseError" % story)
			logging.error(e)
			
		raise ReadLaterException()

	def add(self,story):
		try:
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
			formdata = {"story":story, "selected":"1"}
			data_encoded = urllib.urlencode(formdata)
			
			response = opener.open(URL.URL.READLATER, data_encoded)
			content = response.read()
			root = ET.fromstring(content)
			logging.debug(content)
			try:
				if( root.findall("selected") == [] ):
					raise ReadLaterException()
					
				if( root.findall("selected")[0].text == "1" ):
					logging.info("Added story %s to read-it-later list." % story)
					return True
				else:
					logging.warning("Story %s was already on read-it-later list." % story)
					
			except:
				logging.error("Failed attempting to add story %s to read-it-later list!" % story)
				logging.debug(content)
				
		except ET.ParseError as e:
			logging.error("Failed attempting to add story %s to read-it-later list, xml.etree.ElementTree.ParseError" % story)
			logging.error(e)
			
		raise ReadLaterException()
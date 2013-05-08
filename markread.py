
import credentials
import url as URL
import logging
import urllib2
import urllib

'''
function ToggleRead( _chapter )
{
	var element = $( "#chapter_read_" + _chapter );
	
	$.post('/ajax/toggle_read.php',
	{ 
		chapter: _chapter
	}, 
	function(xml) 
	{ 
		element.attr( "src", xml );
	} 
	);		
	
}
'''

class ChapterReadStateSetFailure(Exception):
	chapterId = None
	def __init__(self, chapterId):
		self.chapterId=chapterId
	def __str__(self):
		return "ChapterReadStateSetFailure(%d)" % self.chapterId

class MarkRead:
	cj = None
	
	def __init__(self, api):
		self.api = api
		self.cj = api.cj

	def mark_read(self, chapterId):
		return self.set_read_state(chapterId, True)

	def mark_unread(self, chapterId):
		return self.set_read_state(chapterId, False)
		
	def set_read_state(self, chapterId, new_read_state):
		intermediate_state = self.toggle(chapterId)
		if intermediate_state == new_read_state:
			return True
		
		# Second toggle, since the read state was already as-intended
		intermediate_state = self.toggle(chapterId)
		if intermediate_state == new_read_state:
			return True
		
		raise ChapterReadStateSetFailure(chapterId)		
	
	def toggle(self, chapterId):
		readurl = URL.URL.READ
		
		responses = {
			'//www.fimfiction-static.net/images/icons/new.png': False,
			'//www.fimfiction-static.net/images/icons/tick.png': True
		}
		
		try:
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
			formdata = {"chapter":chapterId}
			data_encoded = urllib.urlencode(formdata)
		
			response = opener.open(URL.URL.READ, data_encoded)
			content = response.read()
			try:
				new_read_state = responses[content]
				logging.info("Changed chapter %d read state to %s." % (chapterId, new_read_state) )
				return new_read_state
			except:
				logging.error("Failed attempting to change chapter %s state!" % chapterId)

		except Exception as e:
			logging.error(e)

		raise ChapterReadStateSetFailure(chapterId)
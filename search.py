
import urllib
import urlparse
import url as URL

SORT_INITIALDATE="latest"
SORT_HEAT="hot"
SORT_UPDATED="updated"
SORT_TOPRANK="top"
SORT_VIEWCOUNT="views"
SORT_WORDCOUNT="words"
SORT_COMMENTCOUNT="comments"

RATING_ALL="-1"
RATING_EVERYONE="0"
RATING_TEEN="1"
RATING_MATURE="2"

CAT_ALL="0"
CAT_SEX="1"
CAT_GORE="2"

class SearchAPI:
	
	@classmethod	
	def search_url(morepages=0, page=1, search=None, order="updated", romance=None, tragedy=None, sad=None, dark=None, comedy=None, random=None, crossover=None, adventure=None, slice_of_life=None,
		alternate_universe=None, human=None, content_rating=RATING_ALL, mature_categories=CAT_ALL, completed=None, minimum_words=None, maximum_words=None, extra=None, read_it_later=False):
		
		urlbase = URL.URL.SEARCH_BASE # + 'view=category&compact_view=1'
		
		c = {'compact_view':"1", 'view':'category'}
		
		if(search):
			c['search']=search
		
		if(read_it_later==True):
			c['read_it_later'] = "1"
			
		if(completed==True):
			c['completed'] = "1"
		if(romance==True):
			c['category_romance'] = "1"
		else:
			if(romance==False):
				c['category_romance'] = "2"
		if(tragedy==True):
			c['category_tragedy'] = "1"
		else:
			if(tragedy==False):
				c['category_tragedy'] = "2"
		if(sad==True):
			c['category_sad'] = "1"
		else:
			if(sad==False):
				c['category_sad'] = "2"
		if(dark==True):
			c['category_dark'] = "1"
		else:
			if(dark==False):
				c['category_dark'] = "2"
		if(comedy==True):
			c['category_comedy'] = "1"
		else:
			if(comedy==False):
				c['category_comedy'] = "2"
		if(random==True):
			c['category_random'] = "1"
		else:
			if(random==False):
				c['category_random'] = "2"
		if(sad==True):
			c['category_sad'] = "1"
		else:
			if(sad==False):
				c['category_sad'] = "2"
		if(random==True):
			c['category_random'] = "1"
		else:
			if(random==False):
				c['category_random'] = "2"
		if(crossover==True):
			c['category_crossover'] = "1"
		else:
			if(crossover==False):
				c['category_crossover'] = "2"
		if(adventure==True):
			c['category_adventure'] = "1"
		else:
			if(adventure==False):
				c['category_adventure'] = "2"
		if(slice_of_life==True):
			c['category_slice_of_life'] = "1"
		else:
			if(slice_of_life==False):
				c['category_slice_of_life'] = "2"
		if(alternate_universe==True):
			c['category_alternate_universe'] = "1"
		else:
			if(alternate_universe==False):
				c['category_alternate_universe'] = "2"
		if(human==True):
			c['category_human'] = "1"
		else:
			if(human==False):
				c['category_human'] = "2"
		if(slice_of_life==True):
			c['category_slice_of_life'] = "1"
		else:
			if(slice_of_life==False):
				c['category_slice_of_life'] = "2"
		if(slice_of_life==True):
			c['category_slice_of_life'] = "1"
		else:
			if(slice_of_life==False):
				c['category_slice_of_life'] = "2"
		
		if(order):
			c['order'] = order
		if(minimum_words):
			c['minimum_words'] = "%d" % minimum_words
		if(maximum_words):
			c['maximum_words'] = "%d" % maximum_words
		if(mature_categories):
			c['mature_categories'] = mature_categories
		if(content_rating):
			c['content_rating'] = content_rating

		u = urlparse.urlparse(urlbase)
		return urlparse.urlunparse( [u[0],u[1],u[2],u[3],urllib.urlencode(c),u[5] ] )
		
		
"""
Stores the URLs needed to access the site
"""

FIMFICTION = 'http://www.fimfiction.net/'
STATIC     = 'http://www.fimfiction-static.net/'

_DOWNLOAD             = FIMFICTION + 'download_'
DOWNLOAD_TXT          = _DOWNLOAD + 'story.php?story='
DOWNLOAD_HTML         = _DOWNLOAD + 'story.php?html&story='
DOWNLOAD_EPUB         = _DOWNLOAD + 'epub.php?story='
DOWNLOAD_CHAPTER_TXT  = _DOWNLOAD + 'chapter.php?chapter='
DOWNLOAD_CHAPTER_HTML = _DOWNLOAD + 'chapter.php?html&chapter='

SEARCH = FIMFICTION + 'stories?'
STORY  = FIMFICTION + 'story/'

AJAX      = FIMFICTION + 'ajax/'
LOGIN     = AJAX + 'login.php'
READLATER = AJAX + 'add_read_it_later.php'
FAVOURITE = AJAX + 'add_favourite.php'
READ      = AJAX + 'toggle_read.php'
RATE      = AJAX + 'rate.php'

RSS = FIMFICTION + 'rss/'

API_STORY = FIMFICTION + 'api/story.php?story='

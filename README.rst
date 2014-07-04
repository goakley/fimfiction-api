==============
FimFiction-API
==============
--------------
Python API to access FimFiction.net from a Reader's perspective
--------------

Examples
========

::

  from fimfiction.user import User
  from fimfiction.story import Stories, Story
  user = User.load(username)
  storydata = Stories().tracking().unread().search(user)
  story = Story.load(storydata[0]['id'])


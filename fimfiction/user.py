"""
The user module holds basic user information
"""


import http.cookiejar
import urllib

import fimfiction.urls as urls


class User():
    """
    A user of FimFiction.net

    A user is someone who actively participates on the site, consuming the
    content in some way (perhaps by also creating).  Note that this is
    different from an author.  An author is an owner of stories, while a user
    is someone who interacts with the site.  That is, a user and an author hold
    a one-to-one relationship.

    User objects are most useful when authenticated, allowing for
    user-specific actions, such as querying favourite stories.
    """
    @classmethod
    def load(cls, username, password):
        """
        Loads a user from the site with the specified user name

        Username and password are required for authentication.  If you do not
        think you need authentication, you may be looking to use an Author
        object instead.
        """
        user = User(username)
        user.authenticate(password)
        return user

    def __init__(self, username):
        self.username = username
        self._cookie_jar = None
        self._authenticated = False

    def get_request_opener(self):
        """
        Provides a urllib.request.OpenerDirector with this user's cookies

        Use this opener to make requests as the user, useful if the user is
        authenticated.
        """
        cookie_processor = urllib.request.HTTPCookieProcessor(self._cookie_jar)
        return urllib.request.build_opener(cookie_processor)

    def authenticate(self, password):
        """
        Authenticates the user using the given password

        :returns bool: True if authentication was successful, False if not
        :raises ValueError: If unable to authenticate with the given password
        """
        if self._authenticated:
            return

        url = urls.LOGIN

        if self._cookie_jar is None:
            self._cookie_jar = http.cookiejar.CookieJar()

        form_data = {"username": self.username,
                     "password": password,
                     "keep_logged_in": 1}
        form_data_encoded = urllib.parse.urlencode(form_data).encode('ascii')

        opener = self.get_request_opener()
        response = opener.open(url, form_data_encoded).read().decode('ascii')

        if response != "0":
            raise ValueError("Could not authenticate using supplied password")

        self._authenticated = True

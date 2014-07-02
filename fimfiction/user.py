"""
The user module holds basic user information
"""


import http.cookiejar
import urllib

import urls


class User():
    """
    A user of FimFiction.net

    User objects are most useful when authenticated, allowing for
    user-specific actions, such as querying favourite stories.
    """
    def __init__(self, username):
        """
        Creates a user with the specified username
        """
        self.username = username
        self.cookie_jar = None
        self.authenticated = False

    def get_request_opener(self):
        """
        Provides a urllib.request.OpenerDirector with this user's cookies

        Use this opener to make requests as the user, useful if the user is
        authenticated.
        """
        cookie_processor = urllib.request.HTTPCookieProcessor(self.cookie_jar)
        return urllib.request.build_opener(cookie_processor)

    def authenticate(self, password):
        """
        Authenticates the user using the given password

        :return: True if authentication was successful, False if not
        """
        if self.authenticated:
            return True

        url = urls.LOGIN

        if self.cookie_jar is None:
            self.cookie_jar = http.cookiejar.CookieJar()

        form_data = {"username": self.username,
                     "password": password,
                     "keep_logged_in": 1}
        form_data_encoded = urllib.parse.urlencode(form_data).encode('ascii')

        opener = self.get_request_opener()
        response = opener.open(url, form_data_encoded).read().decode('ascii')

        if response != "0":
            return False

        self.authenticated = True
        return True

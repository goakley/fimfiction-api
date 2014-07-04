"""
The story module holds information related to the stories on the site
"""


import datetime
from enum import Enum
import json
import urllib
import re
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

from fimfiction.author import Author
import fimfiction.urls as urls


def utctime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)


class Story():
    """
    Represents a story
    """
    @classmethod
    def load(cls, story_id):
        url = urls.API_STORY + str(story_id)
        opener = urllib.request.build_opener()
        response = opener.open(url, form_data_encoded)
        result = json.load(response)['story']
        result['chapters'] = [
            cha.update(
                {'date_modified': utctime(cha['date_modified'])}
            ) for cha in result['chapters']
        ]
        result['chapters'] = [Chapter(**cha) for cha in result['chapters']]
        result['status'] = cls.Status(result['status'])
        result['categories'] = [
            cls.Category(cat) for cat, ok in result['categories'] if ok
        ]
        result['date_modified'] = utctime(result['date_modified'])
        result['content_rating'] = cls.ContentRating(result['content_rating'])
        result['author'] = Author(result['author'])
        return cls(**result)

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.title = kwargs['title']
        self.short_description = kwargs['short_description']
        self.description = kwargs['description']
        self.chapters = kwargs['chapters']
        self.words = kwargs['words']
        self.date_modified = kwargs['date_modified']
        self.url = kwargs['url']
        self.image_url = kwargs['image']
        self.full_image_url = kwargs['full_image']
        self.views = kwargs['views']
        self.total_views = kwargs['total_views']
        self.likes = kwargs['likes']
        self.dislikes = kwargs['dislikes']
        self.author = kwargs['author']
        # comments

    class Status(Enum):
        incomplete = "Incomplete"
        complete = "Complete"
        on_hiatus = "On Hiatus"

    class Format(Enum):
        """
        The format of a rendered/downloaded story
        """
        txt = 1
        html = 2
        epub = 3

    class Category(Enum):
        random = "Random"
        romance = "Romance"
        alternate_universe = "Alternate Universe"
        slice_of_life = "Slice of Life"
        comedy = "Comedy"
        crossover = "Crossover"
        dark = "Dark"
        tragedy = "Tragedy"
        adventure = "Adventure"
        human = "Human"
        sad = "Sad"
        anthro = "Anthro"

    def download(self, story_format=Format.txt):
        """
        Provides the contents of the story in a certain format

        :param Story.Format format: Which format to provide
        """
        if story_format == Story.Format.txt:
            url = urls.DOWNLOAD_TXT
        elif story_format == Story.Format.html:
            url = urls.DOWNLOAD_HTML
        elif story_format == Story.Format.epub:
            url = urls.DOWNLOAD_EPUB
        url += str(self.identity)
        opener = urllib.request.build_opener()
        response = opener.open(url).read().decode('utf-8')
        return response

    def favourite(self, user, active=True):
        """
        Change the favourite status of this story for a use

        :param bool active: Whether this story should be a favourite
        """
        url = urls.FAVOURITE
        target_state = 1 if active else 0
        opener = user.get_request_opener()
        form_data = {'story': self.identity, 'selected': str(target_state)}
        form_data_encoded = urllib.parse.urlencode(form_data).encode('ascii')
        response = opener.open(url, form_data_encoded).read().decode('ascii')

        try:
            status = int(ET.fromstring(response).find('selected').text)
        except AttributeError:
            return False
        return status == target_state

    def read_later(self, user, active=True):
        """
        Change the 'read later' status of this story for a user

        :param bool active: Whether this story should be a 'read later' story
        """
        url = urls.READLATER
        target_state = 1 if active else 0
        opener = user.get_request_opener()
        form_data = {'story': self.identity, 'selected': str(target_state)}
        form_data_encoded = urllib.parse.urlencode(form_data).encode('ascii')
        response = opener.open(url, form_data_encoded).read().decode('ascii')

        try:
            status = int(ET.fromstring(response).find('selected').text)
        except AttributeError:
            return False
        return status == target_state


class Chapter():
    """
    Represents a chapter in a story

    Note: Chapter identities are NOT the number of the chapter in a story.
    """
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.title = kwargs['title']
        self.link = kwargs['link']
        self.words = kwargs['words']
        self.views = kwargs['views']
        self.date_modified = kwargs['date_modified']

    def mark_read(self, user):
        """
        Marks this chapter as read by the user
        """
        return self._toggle_to_state(user.get_request_opener(), 1)

    def mark_unread(self, user):
        """
        Marks this chapter as unread by the user stored in the opener
        """
        return self._toggle_to_state(user.get_request_opener(), 0)

    def _toggle_to_state(self, opener, state):
        """
        Toggles the is_read flag until it reaches a state
        """
        url = urls.READ
        form_data = {'chapter': self.identity}
        form_data_encoded = urllib.parse.urlencode(form_data).encode('ascii')
        response = opener.open(url, form_data_encoded).read().decode('ascii')

        try:
            status = int(ET.fromstring(response).find('read').text)
        except AttributeError:
            return False
        if status != state:
            self._toggle_to_state(opener, state)
        return True


class Stories():
    """
    Acts as a way of fetching a set of stories

    This class's purpose is to fetch a set of stories based on some criteria.
    The methods of this class are designed to be chained together, terminated
    with a call to `execute` (optionally) passing in a user.  Example:

    Stories().tracking().unread().order('updated').search(user)

    Certian attributes, such as `tracking`, will only work in a search using an
    authenticated User object.
    """
    def __init__(self):
        self.options = {}

    class ContentRating(Enum):
        """
        The content / subject matter rating of a story
        """
        everyone = 3
        teen = 1
        mature = 2

    class Order(Enum):
        """
        The format of a rendered/downloaded story
        """
        latest = "latest"
        hot = "hot"
        updated = "updated"
        top = "top"
        views = "views"
        words = "words"
        comments = "comments"

    def search(self, text):
        self.options['search'] = text
        return self

    def tracking(self):
        """
        Toggles only stories tracked by the searching user
        """
        self.options['tracking'] = 1
        return self

    def read_it_later(self):
        """
        Toggles only stories in the searching user's "read-it-later" list
        """
        self.options['read_it_later'] = 1
        return self

    def unread(self):
        """
        Toggles only stories unread by the searching user
        """
        self.options['unread'] = 1
        return self

    def order(self, order):
        """
        Sorts results by the given Order
        """
        self.options['order'] = order.name
        return self

    def content_rating(self, rating):
        """
        Filters results to the given ContentRating
        """
        self.options['content_rating'] = rating.value
        return self

    def completed(self):
        """
        Allows only stories that are completed
        """
        self.options['completed'] = 'on'
        return self

    def minimum_words(self, limit):
        """
        Allows only stories with `limit` number of words
        """
        self.options['minimum_words'] = str(limit)
        return self

    def maximum_words(self, limit):
        """
        Allows only stories with less than `limit` number of words
        """
        self.options['maximum_words'] = str(limit)
        return self

    def sex(self):
        """
        Allows stories with sex
        """
        self.options['sex'] = 1
        return self

    def gore(self):
        """
        Allows stories with gore
        """
        self.options['gore'] = 1
        return self

    def category(self, category):
        """
        Allows stories in a specific category
        """
        self.options['category_' + category.name.lower()] = 1
        return self

    def execute(self, user=None, limit=20, page=1):
        """
        Executes a search based on the criteria specified

        :return: A list of dictionary items (name, id, author)
        """
        if limit <= 0:
            return []
        url = urls.SEARCH
        opener = user.get_request_opener() if user is not None \
                 else urllib.request.build_opener()
        options = self.options.copy()
        options['page'] = page
        form_data = urllib.parse.urlencode(options)
        response = opener.open(url + form_data).read()
        soup = BeautifulSoup(response)
        titles = soup.find_all('div', class_='title', id=None)
        if not titles:
            return []
        result = []
        for title in titles:
            id_str = title.find('a', class_='story_name')['href']
            result.append({
                'name': title.find('a', class_='story_name').get_text(),
                'id': int(re.search('/story/(.+?)/', id_str).group(1)),
                'author': title.find('span', class_='author').get_text()
            })
        limit -= len(result)
        return result + self.search(opener, limit=limit, page=page+1)

"""
The author module holds author information
"""


class Author():
    """
    An author on FimFiction.net

    An author is someone who writes for the site.  Note that this is different
    from a user, who uses the site generically.  A user and an author have a
    one-to-one relationship.
    """
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']

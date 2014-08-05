"""
The author module holds author information
"""


class Author():
    """
    An author on FimFiction.net

    An author is and entity on the site that has some number of stories
    associated with them.  Note that this is different from a user, who
    from a user, who consumes and provides content on the site.  A user and an
    author have a one-to-one relationship.
    """
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']

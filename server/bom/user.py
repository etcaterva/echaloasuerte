import logging
import hashlib

from django.contrib.auth.hashers import check_password, make_password
from django.utils.http import urlencode

logger = logging.getLogger("echaloasuerte")


class User(object):
    """
    Main user within echaloasuerte
    """

    @property
    def favourites_list(self):
        try:
            rd = server.mongodb.driver.MongoDriver.instance().retrieve_draw
            return [rd(f) for f in self.favourites]
        except Exception as e:
            logger.error(
                "Error when retrieving the list of favourites for user {0}. {1}".format(
                    self.pk, e))
            return []

    @property
    def pk(self):
        return str(self._id)

    def save(self, **args):
        pass

    @property
    def user_image(self):
        """Returns a picture that identifies the user
        If the user doesn't use Gravatar, a random image based on it's email will be shown"""
        default = "monsterid"
        size = 85
        email = self.email.lower()
        gravatar_url = "//www.gravatar.com/avatar/" + hashlib.md5(
            email.encode('utf-8')).hexdigest() + "?"
        parameters = {'d': default,
                      's': str(size)}
        if not self.use_gravatar:
            parameters['f'] = 'y'
        gravatar_url += urlencode(parameters)
        return gravatar_url

    def __init__(self, _id, password=None, favourites=None, alias=None,
                 use_gravatar=True):
        self._id = _id
        """Email of the user"""

        self.password = password
        """encripted password of the user"""

        self.favourites = favourites if favourites is not None else []
        """List of favourites of a user"""

        if alias:
            self.alias = alias
            """Alias of the user (name it appears for the public)"""
        else:
            self.alias = str(_id).split('@')[0]

        self.use_gravatar = use_gravatar
        """Permission from the user to use his Gravatar"""

    @property
    def email(self):
        return self._id

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self._id


import server.mongodb.driver

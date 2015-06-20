from django.contrib.auth.hashers import (check_password, make_password)

import logging
import urllib
import hashlib
logger = logging.getLogger("echaloasuerte")

def gravatar(email):
    default = "http://example.com/static/images/defaultavatar.jpg"
    size = 100
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return gravatar_url


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
            logger.error("Error when retrieving the list of favourites for user {0}. {1}".format(self.pk,e))
            return []
    @property
    def pk(self):
        return str(self._id)

    def save(self,**args):
        pass

    @property
    def user_image(self):
        """Returns a picture that identifies the usre
        Either the self.avatar url or a gravatar one"""
        if self.avatar:
            return self.avatar
        else:
            return gravatar(self.get_email())

    def __init__(self, _id, password = None, favourites = None, alias=None, avatar=None):
        self._id = _id
        """Email of the user"""

        self.password = password
        """encripted password of the user"""

        self.favourites = favourites if favourites is not None else []
        """List of favourites of a user"""

        self.alias = alias if alias else self._id
        """Alias of the user (name it appears for the public)"""

        self.avatar = avatar
        """Picture that represents the user"""

    def get_email(self):
        return self._id

    def get_username(self):
        try:
            return self._id.split('@')[0]
        except Exception as e:
            return self._id

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def check_password(self,raw_password):
        return check_password(raw_password, self.password)

    def set_password(self,raw_password):
        self.password = make_password(raw_password)

    def __str__(self):

        return self.get_username()


import server.mongodb.driver

from django.contrib.auth.hashers import (check_password, make_password)

import logging
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
            logger.error("Error when retrieving the list of favourites for user {0}. {1}".format(self.pk,e))
            return []
    @property
    def pk(self):
        return str(self._id)

    def save(self,**args):
        pass

    def __init__(self, _id, password = None, favourites = None ):
        self._id = _id
        """Email of the user"""

        self.password = password
        """encripted password of the user"""

        self.favourites = favourites if favourites is not None else []
        """List of favourites of a user"""

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

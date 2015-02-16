from django.core.mail import send_mail
from django.contrib.auth.hashers import (check_password, make_password)
from django.utils.translation import ugettext_lazy as _
import random
import datetime
#from server.mongodb.driver import *

class User(object):
    """
    Main user within echaloasuerte
    """

    @property
    def pk(self):
        return str(self._id)

    def save(self,**args):
        pass

    def __init__(self, _id, password = None, favorites = None ):
        self._id = _id
        """Email of the user"""

        self.password = password
        """encripted password of the user"""
        
        self.favorites = favorites if favorites is not None else []
        """List of favorites of a user"""

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

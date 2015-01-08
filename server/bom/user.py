from django.core.mail import send_mail
from django.contrib.auth.hashers import (check_password, make_password)
from django.utils.translation import ugettext_lazy as _
import random
import datetime

class User(object):
    """
    Main user within echaloasuerte
    """

    def __init__(self, email, password = None):

        self.email = email
        """Email of the user"""

        self.password = password
        """encripted password of the user"""

    def get_username(self):
        return self.email

    def is_anonymous(self):
        return True

    def is_authenticated(self):
        return False

    def get_username(self):
        return self.username

    def check_password(self,raw_password):
        return check_password(raw_password, self.password)

    def set_password(self,raw_password):
        self.password = make_password(raw_password)

    def __str__(self):
        return self._get_username()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

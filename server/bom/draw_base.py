from django.utils.translation import ugettext_lazy as _
import random
import datetime
from abc import ABCMeta, abstractmethod
import logging
logger = logging.getLogger("echaloasuerte")
import pytz

def get_utc_now():
    return datetime.datetime.utcnow().replace(tzinfo = pytz.utc)

class BaseDraw(object):
    """
    Stores the content of a draw of random items
    """
    __metaclass__ = ABCMeta

    def __init__(self, creation_time = None, owner = None, number_of_results = 1,
                  results= None, _id = None, draw_type = None, prev_draw = None,
                  users = None, title = None, password=None, shared_type = None,
                  show_in_public_list = True, enable_chat = True, last_updated_time=None,
                  audit = None):
        self.number_of_results = number_of_results
        """Number of results to generate"""

        self.results = results if results is not None else []
        """List of results (list of list of items)"""

        self._id = _id
        """Unique identifier of the draw"""

        self.owner = owner
        """ID of the owner of the draw"""

        self.draw_type = type(self).__name__
        """Type of the draw"""

        self.creation_time = creation_time if creation_time is not None else datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        """Time the draw was created"""

        self.last_updated_time = last_updated_time if last_updated_time else self.creation_time
        """last time this draw was updated"""

        self.prev_draw = prev_draw
        """Id of the prev draw that was modified creating this one"""

        self.users = users if users is not None else []
        """List of users with access to the draw"""

        self.title = title
        """Title of the concrete draw"""

        self.password = password
        """Password of the public draw"""

        self.audit = audit if audit is not None else []
        """List of changes in the draw main config, user add_audit to add items"""

        self.show_in_public_list = show_in_public_list
        """Wether or not to display the draw in the public lists of draws"""

        self.enable_chat = enable_chat
        """Wether or not to display the chat"""

        self.shared_type = shared_type
        '''Type of shared type. None, Public, Invite'''

        '''
        shared_type  password   Descr:
        -------------------------------
        None         N/A        Single user draw
        Invite       N/A        Only invited users can access
        Public       N          Anybody can access
        Public       Y          Either users or password
        '''

        #TODO: remove me in the future, PLEASE
        if self.shared_type == "None" or self.shared_type == "":
            self.shared_type = None
        if draw_type and draw_type != self.draw_type:
            logger.warning("A draw was built with type {0} but type {1} was "
                           "passed as argument! Fix it!".format(
                               draw_type, self.draw_type))
        if self.last_updated_time.tzinfo is None:
            self.last_updated_time.replace(tzinfo=pytz.utc)
        if self.creation_time.tzinfo is None:
            self.creation_time.replace(tzinfo=pytz.utc)

    @property
    def pk(self):
        return str(self._id)

    def is_shared(self):
        return self.shared_type is not None

    @property
    def share_settings(self):
        return {
                "shared_type" : self.shared_type,
                "password" : bool(self.password),
                "show_in_public_list" : self.show_in_public_list,
                "enable_chat" : self.enable_chat
                }

    def user_can_read(self, user, password=None):
        '''Checks for read access'''
        if self.shared_type is None:
            #Only owner can access
            return self.user_can_write(user)
        else:
            #Listed users/owner can access
            if user.is_authenticated():
                if user.pk == self.owner:
                    return True
                if user.pk in self.users:
                    return True

            #If password base, check password
            if self.password:
                return self.password == password

            #All check failed, lets check if public
            return self.shared_type == 'Public'

    def user_can_write(self, user):
        '''Checks whether user can write'''
        if self.owner is None:
            return True
        return user.pk == self.owner

    def is_feasible(self):
        return self.number_of_results > 0

    def mark_updated(self):
        """updated the last_updated_time of the draw to now"""
        self.last_updated_time = get_utc_now()

    def add_audit(self, type_):
        """Adds an audit message for the modification of a draw
        The latest audit are at the begining
        the type of audits are:
        SETTINGS_CONFIG: Something changed related to the config of the draw
        DRAW_PARAMETERS: one or more of the basic parameters of the draw changed
        """
        self.audit.insert(0, {
            "type": type_,
            "datetime": get_utc_now()
        })
        self.mark_updated()

    def toss(self):
        result = {"datetime": get_utc_now(), "items": self.generate_result()}
        self.results.append(result)
        logger.debug("Tossed draw: {0}".format(self))
        return result

    @abstractmethod
    def generate_result(self):
        """This should return a list of generated results"""
        pass

    def __str__(self):
        return str(self.__dict__)

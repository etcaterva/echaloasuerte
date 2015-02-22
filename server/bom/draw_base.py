from django.utils.translation import ugettext_lazy as _
import random
import datetime
from abc import ABCMeta, abstractmethod
import logging
logger = logging.getLogger("echaloasuerte")
import django.utils.timezone
import pytz

class BaseDraw(object):
    """
    Stores the content of a draw of random items
    """
    __metaclass__ = ABCMeta
    DEFAULT_TITLE = None

    @property
    def pk(self):
        return str(self._id)

    def __init__(self, creation_time = None, owner = None, number_of_results = 1,
                  results= None, _id = None, draw_type = None, prev_draw = None,
                  users = None, title = None, password=None, shared_type = 'None'):
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

        self.creation_time = creation_time if creation_time is not None else django.utils.timezone.now()
        """Time the draw was created"""
        self.creation_time.replace(tzinfo=pytz.utc)

        self.prev_draw = prev_draw
        """Id of the prev draw that was modified creating this one"""

        self.users = users if users is not None else []
        """List of users with access to the draw"""

        self.title = title
        """Title of the concrete draw"""

        self.password = password
        """Password of the public draw"""

        if draw_type and draw_type != self.draw_type:
            logger.warning("A draw was built with type {0} but type {1} was passed as argument! Fix it!".format(draw_type,self.draw_type))

        #if self.title is None:
        #    logger.warning("Draw with id {0} and type {1} have no title".format(self._id,str(type(self).__name__)))

        self.shared_type = shared_type
        '''Type of shared type. None, Public, Invite'''

        '''
        shared_type  password   Descr:
        -------------------------------
        None         N/A        Single user draw
        Public       N          Anybody can access
        Public       Y          Only users with password can access
        Invite       N          Only invited users can access
        Invite       Y          Either users or password
        '''

    def user_can_read(self, user, password = None):
        '''Checks for read access'''
        if self.shared_type == 'None':
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

    def toss(self):
        result = {"datetime": datetime.datetime.utcnow(), "items": self.generate_result()}
        self.results.append(result)
        logger.debug("Tossed draw: {0}".format(self))
        return result

    @abstractmethod
    def generate_result(self):
        """This should return a list of generated results"""
        pass

    def __str__(self):
        return str(self.__dict__)

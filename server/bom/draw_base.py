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

    @property
    def pk(self):
        return str(self._id)

    def __init__(self, creation_time = None, owner = None, number_of_results = 1, results= None, _id = None, draw_type = None):
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

        if draw_type and draw_type != self.draw_type:
            logger.warning("A draw was built with type {0} but type {1} was passed as argument! Fix it!".format(draw_type,self.draw_type))

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

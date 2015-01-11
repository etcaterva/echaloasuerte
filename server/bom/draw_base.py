from django.utils.translation import ugettext_lazy as _
import random
import datetime
from abc import ABCMeta, abstractmethod
import logging
logger = logging.getLogger("echaloasuerte")

class BaseDraw(object):
    """
    Stores the content of a draw of random items
    """
    __metaclass__ = ABCMeta

    def __init__(self, number_of_results = 1, results= None, _id = None):
        self.number_of_results = number_of_results
        """Number of results to generate"""

        self.results = results if results is not None else []
        """List of results (list of list of items)"""

        self._id = _id
        """Unique identifier of the draw"""

    def is_feasible(self):
        return self.number_of_results > 0

    def toss(self):
        result = {"datetime": datetime.datetime.utcnow(), "items": self.generate_result()}
        self.results.append(result)
        logger.debug("Tossed draw: {0}".format(self.results))
        return result

    @abstractmethod
    def generate_result(self):
        """This should return a list of generated results"""
        pass

    def __str__(self):
        return str(self.__dict__)

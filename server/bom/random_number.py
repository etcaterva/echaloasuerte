from django.utils.translation import ugettext_lazy as _
import random


class RandomNumberDraw(object):
    """
    Class that represents a draw with the details to produce random numbers.
    """
    def __init__(self,range_min=0,range_max=None,number_of_results=1,allow_repeat=False):
        self.range_min = range_min
        """"Minimun value to be generated. Inclusive."""

        self.range_max = range_max
        """"Maximun value to be generated. Exclusive."""

        self.number_of_results = number_of_results
        """Number of Random numbers to generate"""

        self.allow_repeat = allow_repeat
        """Whether the set of numbers to generate can contain repetitions. Note, if false, max-min > num_res"""


    def is_feasible(self):
        if self.range_max is None:
            return False
        if self.allow_repeat == True:
            return self.range_min < self.range_max
        else:
            return self.range_max - self.range_min >= self.number_of_results


    def toss(self):
        """Carries out the toss"""
        pass

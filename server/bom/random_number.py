from django.utils.translation import ugettext_lazy as _
import random
import datetime
from server.bom.draw_base import *


class RandomNumberDraw(BaseDraw):
    """
    Class that represents a draw with the details to produce random numbers.
    """

    def __init__(self, range_min=0, range_max=None, allow_repeat=False, **kwargs):
        super(RandomNumberDraw, self).__init__(**kwargs)

        self.range_min = range_min
        """"Minimun value to be generated. Inclusive."""

        self.range_max = range_max
        """"Maximun value to be generated. Inclusive."""

        self.allow_repeat = allow_repeat
        """Whether the set of numbers to generate can contain repetitions. Note, if false, max-min > num_res"""

    def is_feasible(self):
        if self.range_max is None:
            return False
        if self.allow_repeat == True:
            return self.range_min < self.range_max
        else:
            return self.range_max - self.range_min >= self.number_of_results


    def generate_result(self):
        """Carries out the toss"""
        result = []
        for i in range(0, self.number_of_results):
            while True:
                random_value = random.randint(self.range_min, self.range_max)
                if (self.allow_repeat or random_value not in result):
                    result.append(random_value)
                    break
        return result

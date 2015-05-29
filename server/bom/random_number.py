from django.utils.translation import ugettext_lazy as _
import random
from server.bom.draw_base import *


class RandomNumberDraw(BaseDraw):
    """
    Class that represents a draw with the details to produce random numbers.
    """

    def __init__(self, range_min=0, range_max=10, allow_repeat=False, **kwargs):
        super(RandomNumberDraw, self).__init__(**kwargs)

        self.range_min = range_min
        """"Minimun value to be generated. Inclusive."""

        self.range_max = range_max
        """"Maximun value to be generated. Inclusive."""

        self.allow_repeat = allow_repeat
        """Whether the set of numbers to generate can contain repetitions. Note, if false, max-min > num_res"""

    def is_feasible(self):
        #TODO range_max must have a defaulf value
        if self.number_of_results <= 0:
            # At least one result is requested
            return False

        if self.number_of_results > 50:
            # Too many results
            return False

        if self.allow_repeat:
            if self.range_min >= self.range_max:
                # Range is too small
                return False
        else:
            if self.range_max - self.range_min < self.number_of_results:
                # Range is too small, do you want to allow repeated numbers?
                return False

        return True


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

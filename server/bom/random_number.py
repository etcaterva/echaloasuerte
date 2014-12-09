from django.utils.translation import ugettext_lazy as _
import random
import datetime


class RandomNumberDraw(object):
    """
    Class that represents a draw with the details to produce random numbers.
    """
    def __init__(self,range_min=0,range_max=None,number_of_results=1,allow_repeat=False, results=None):
        self.range_min = range_min
        """"Minimun value to be generated. Inclusive."""

        self.range_max = range_max
        """"Maximun value to be generated. Inclusive."""

        self.number_of_results = number_of_results
        """Number of Random numbers to generate"""

        self.allow_repeat = allow_repeat
        """Whether the set of numbers to generate can contain repetitions. Note, if false, max-min > num_res"""

        self.results = results if results is not None else []
        """Results of the draw"""

        self.draw_type = "random_number"
        """Never modified, but will be used when deserialising."""


    def is_feasible(self):
        if self.range_max is None:
            return False
        if self.allow_repeat == True:
            return self.range_min < self.range_max
        else:
            return self.range_max - self.range_min >= self.number_of_results


    def toss(self):
        """Carries out the toss"""
        result = {"datetime":datetime.datetime.utcnow(),"numbers":[]}
        for i in range(0, self.number_of_results):
            while True:
                random_value = random.randint(self.range_min, self.range_max)
                if (self.allow_repeat or random_value not in result["numbers"]):
                    result["numbers"].append(random_value)
                    break
        #print "Generated: {0} \nFor Draw: {1}".format(result,self.__dict__)
        self.results.append(result)
        return result

from django.db import models

class RandonNumberDraw(models.Model):
    pass
class RandomNumberPoll(models.Model):
    """
    Class that represents a poll with the details to produce random numbers.
    """

    range_min = models.BigIntegerField("Range start", blank=False, null=False, default=0)
    """"Minimun value to be generated. Inclusive."""

    range_max = models.BigIntegerField("Range End", blank=False, null=False)
    """"Maximun value to be generated. Exclusive."""

    number_of_results = models.PositiveIntegerField("Number of results", blank=False, null=False, default=1)
    """Number of Random numbers to generate"""

    allow_repeat = models.BooleanField("Allow Repetitions", blank=False, null=False, default=False)
    """Whether the set of numbers to generate can contain repetitions. Note, if false, max-min > num_res"""

    def is_feasible(self):
        if self.range_max is None:
            return False
        if self.allow_repeat == True:
            return True
        else:
            return self.range_max - self.range_min >= self.number_of_results


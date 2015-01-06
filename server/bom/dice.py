
from django.utils.translation import ugettext_lazy as _
import random
import datetime

class DiceDraw(object):
    """
    Stores the content of a draw of Dice
    """

    def __init__(self, number_of_results = 1, results = None):

        self.number_of_results = number_of_results
        """Number of dices to get"""

        self.results = results if results is not None else []
        """resuls of the draws"""

    def is_feasible(self):
        return self.number_of_results > 0

    def toss(self):
        result = {"datetime": datetime.datetime.utcnow(), "result": [random.randint(1,6) for x in range(0,self.number_of_results)] }
        self.results.append(result)
        return result

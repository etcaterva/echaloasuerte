
from django.utils.translation import ugettext_lazy as _
import random
import datetime

class CoinDraw(object):
    """
    Stores the content of a draw of Coin
    """

    def __init__(self, number_of_results = 1,results = None):

        self.number_of_results = number_of_results
        """number of results to generate"""

        self.results = results if results is not None else []
        """resulsts"""

    def is_feasible(self):
        return self.number_of_results > 0

    def toss(self):
        for i in range(0,self.number_of_results):
            result = {"datetime": datetime.datetime.utcnow(), "result": random.choice([_('head'),_('tail')])}
            self.results.append(result)
            return result

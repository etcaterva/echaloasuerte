from django.utils.translation import ugettext_lazy as _
import random
import datetime

class RandomItemDraw(object):
    """
    Stores the content of a draw of random items
    """
    def __init__(self, items= [], number_of_results = 1, allow_repeat=False, results= None):
        self.items = items
        """Source items of the draw"""

        self.number_of_results = number_of_results
        """Number of results to generate"""

        self.allow_repeat = allow_repeat
        """Whether the same item can appear more than once in the result"""

        self.results = results if results is not None else []
        """List of results (list of list of items)"""

    def is_feasible(self):
        if len(self.items) == 0:
            return False
        return self.number_of_results <= len(self.items) or self.allow_repeat

    def toss(self):
        result = {"datetime": datetime.datetime.utcnow(), "items": []}
        for i in range(0,self.number_of_results):
            while True:
                random_value = random.choice(self.items)
                if (self.allow_repeat or random_value not in result["items"]):
                    result["items"].append(random_value)
                    break
        # print "Generated: {0} \nFor Draw: {1}".format(result,self.__dict__)
        self.results.append(result)
        return result

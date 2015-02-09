from django.utils.translation import ugettext_lazy as _
import random
import datetime
from server.bom.draw_base import *


class RandomItemDraw(BaseDraw):
    """
    Stores the content of a draw of random items
    """
    DEFAULT_TITLE= _("""Random Item""")

    def __init__(self, items= [], allow_repeat=False, **kwargs):
        super(RandomItemDraw, self).__init__(**kwargs)

        self.items = items
        """Source items of the draw"""

        self.allow_repeat = allow_repeat
        """Whether the same item can appear more than once in the result"""

    def is_feasible(self):
        if len(self.items) <= 0 or self.number_of_results <= 0:
            return False
        return self.number_of_results <= len(self.items) or self.allow_repeat

    def generate_result(self):
        result = []
        for i in range(0,self.number_of_results):
            while True:
                random_value = random.choice(self.items)
                if (self.allow_repeat or random_value not in result):
                    result.append(random_value)
                    break
        return result


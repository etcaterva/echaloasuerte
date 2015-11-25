import random
import itertools
from server.bom.draw_base import BaseDraw, InvalidDraw


class GroupsDraw(BaseDraw):
    """Stores the content of a draw to create groups

    The number of results corresponds to the number of
    groups to generate
    """
    TYPES = BaseDraw.TYPES.copy()
    TYPES['items'] = list

    def __init__(self, items=None, **kwargs):
        super(GroupsDraw, self).__init__(**kwargs)

        self.items = items if items else []
        """Source items of the draw"""

    def validate(self):
        super(GroupsDraw, self).validate()
        if not self.items:
            raise InvalidDraw('items')
        if self.number_of_results > len(self.items):
            raise InvalidDraw('number_of_results')

    def is_feasible(self):
        if len(self.items) <= 0 or self.number_of_results <= 0:
            return False
        return self.number_of_results <= len(self.items)

    def generate_result(self):
        result = [list() for _ in range(self.number_of_results)]
        items = self.items[:]
        random.shuffle(items)
        for group, item in zip(itertools.cycle(result), items):
            group.append(item)
        return result

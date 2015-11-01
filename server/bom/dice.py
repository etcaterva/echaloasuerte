import random

from server.bom.draw_base import BaseDraw, InvalidDraw


class DiceDraw(BaseDraw):
    """
    Stores the content of a draw of Dice
    """

    def __init__(self, **kwargs):
        super(DiceDraw, self).__init__(**kwargs)

    def validate(self):
        super(DiceDraw, self).validate()
        if self.number_of_results > 20:
            raise InvalidDraw('number_of_results')

    def is_feasible(self):
        return 0 < self.number_of_results < 20

    def generate_result(self):
        return [random.randint(1, 6) for x in range(0, self.number_of_results)]

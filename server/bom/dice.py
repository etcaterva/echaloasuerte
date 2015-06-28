from server.bom.draw_base import *


class DiceDraw(BaseDraw):
    """
    Stores the content of a draw of Dice
    """

    def __init__(self, **kwargs):
        super(DiceDraw, self).__init__(**kwargs)

    def is_feasible(self):
        return 0 < self.number_of_results < 20

    def generate_result(self):
        return [random.randint(1, 6) for x in range(0, self.number_of_results)]

from server.bom.draw_base import *


class CoinDraw(BaseDraw):
    """
    Stores the content of a draw of Coin
    """

    def __init__(self, **kwargs):
        super(CoinDraw, self).__init__(**kwargs)

    def is_feasible(self):
        return 0 < self.number_of_results < 10

    def generate_result(self):
        return [random.choice(['head', 'tail']) for x in range(0, self.number_of_results)]

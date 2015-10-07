import random
import string
from server.bom.draw_base import BaseDraw, InvalidDraw


class RandomLetterDraw(BaseDraw):
    """
    Class that represents a draw with the details to produce random letters.
    """

    def __init__(self, **kwargs):
        super(RandomLetterDraw, self).__init__(**kwargs)

    def validate(self):
        super(RandomLetterDraw, self).validate()
        if self.number_of_results > 50:
            raise InvalidDraw('number_of_results')

    def is_feasible(self):
        if self.number_of_results <= 0:
            # At least one result is requested
            return False
        if self.number_of_results > 50:
            # Too many results
            return False
        return True

    def generate_result(self):
        """Carries out the toss"""
        return [random.choice(string.ascii_letters)
                for _ in range(self.number_of_results)]

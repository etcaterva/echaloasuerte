import random

from django.utils.translation import ugettext_lazy as _

from server.bom.draw_base import BaseDraw, InvalidDraw


class SpinnerDraw(BaseDraw):
    """
    Class that represents a draw with the details to produce an angle.
    """
    TYPES = BaseDraw.TYPES.copy()

    def __init__(self, range_min=0, range_max=10, allow_repeat=False, **kwargs):
        super(SpinnerDraw, self).__init__(**kwargs)

    def validate(self):
        super(SpinnerDraw, self).validate()

    def is_feasible(self):
        return True

    def generate_result(self):
        """Carries out the toss"""
        return [random.randint(0, 360)]

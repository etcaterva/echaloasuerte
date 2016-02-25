import random
from server.bom.draw_base import BaseDraw, InvalidDraw


class PhotoDraw(BaseDraw):
    """Class that represents a draw with the details to produce points in a photo
    """
    TYPES = BaseDraw.TYPES.copy()

    def __init__(self, photo_url=None, **kwargs):
        super(PhotoDraw, self).__init__(**kwargs)
        self.photo_url = photo_url or ""

    def validate(self):
        super(PhotoDraw, self).validate()
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
        result = []
        for i in range(0, self.number_of_results):
            while True:
                random_point = (random.randint(0, 100), random.randint(0, 100))
                if random_point not in result:
                    result.append(random_point)
                    break
        return result

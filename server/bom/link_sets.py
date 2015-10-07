from server.bom.draw_base import BaseDraw, InvalidDraw
from random import shuffle
from itertools import cycle
import logging

logger = logging.getLogger("echaloasuerte")


class LinkSetsDraw(BaseDraw):
    """
    Stores the content of a draw of LinkSetsDraw
    It associates items from several sets.
    Sets are provided as a list of lists
    E.g:
    Set A: 1,2,3
    Set B: a,b,c
    Set C: Y,X,Z
    should produce: [ [1,b,c] [2,c,Y] [3,a,X] ]


    number of results is meaningless for this kind of draw
    note: The first set drives the draw.
        - The number of results generated will be equal to the number of items in the first set
        - If needed, items will be added to the others set or ignored to match the length of the first
    """
    TYPES = BaseDraw.TYPES.copy()
    TYPES['sets'] = list

    def __init__(self, sets=None, **kwargs):
        super(LinkSetsDraw, self).__init__(**kwargs)

        self.sets = sets if sets else []
        """List of sets of items to associate"""

        self.number_of_results = 1  # meaningless

        # validation
        try:
            if sets:
                for i in sets:
                    i[0]  # validate is a list and has at least 1 element
        except Exception as e:
            logger.error("Issue when creating a LinkSetsDraw."
                         " Items: {0}, exception: {1}".format(sets, e))

    def validate(self):
        super(LinkSetsDraw, self).validate()
        if not self.sets or not self.sets[0]:
            raise InvalidDraw('sets')

    def is_feasible(self):
        return self.sets and len(self.sets[0]) > 0 and len(self.sets) > 1

    def generate_result(self):
        sets = [list(self.sets[0])]  # No changes to the first
        sets[1:] = [list(x) for x in self.sets[1:]]  # Copy
        for s in sets[1:]:
            shuffle(s)  # Shuffle change in place
        sets[1:] = [cycle(x) for x in sets[1:]]  # create iterator
        return list(zip(*sets))  # list needed for python 3


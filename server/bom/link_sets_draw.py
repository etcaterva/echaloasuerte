from django.utils.translation import ugettext_lazy as _
import random
import datetime
from server.bom.draw_base import *
from random import shuffle
from itertools import cycle
import logging
logger = logging.getLogger("echaloasuerte")

class LinkSetsDraw(BaseDraw):
    """
    Stores the content of a draw of LinkSetsDraw
    It asociates items from several sets.
    Sets are provided as a list of lists
    E.g:
    Set A: 1,2,3
    Set B: a,b,c
    Set C: Y,X,Z
    should produce: [ [1,b,c] [2,c,Y] [3,a,X] ]


    number of results is meaningless for this kind of draw
    note: The first set drives the draw.
        - The numer of results generated will be equal to the number of items in the first set
        - If needed, items will be added to the others set or ignoted to match the length of the first
    """

    def __init__(self, sets=[], **kwargs):
        super(LinkSetsDraw, self).__init__(**kwargs)

        self.sets = sets
        """List of sets of items to asociate"""

        self.number_of_results = None #Override as meaningless

        #validation
        try:
            if sets:
                for i in sets:
                    i[0] #validate is a list and has at least 1 element
        except Exception as e:
            logger.error("Issue when creating a AsociationListDraw. Items: {0}, exception: {1}".format(sets,e))

    def is_feasible(self):
        return self.sets and len(self.sets[0]) > 0 and len(self.sets) > 1

    def generate_result(self):
        sets = [list(self.sets[0])]
        sets[1:] = [list(x) for x in self.sets[1:] ]
        for s in sets[1:]: shuffle(s)
        sets[1:] = [cycle(x) for x in sets[1:] ]
        return zip(*sets)


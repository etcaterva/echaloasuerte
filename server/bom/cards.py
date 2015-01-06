from django.utils.translation import ugettext_lazy as _
import random
import datetime


class CardsDrawDraw(object):
    """
    Stores the content of a draw of CardsDraw
    """

    def __init__(self, type_of_deck=1, number_of_results=1):

        self.type_of_deck = type_of_deck
        """Type of deck to be used"""

        self.number_of_results = number_of_results
        """Number of cards to be drawn"""

    def is_feasible(self):
        pass

    def toss(self):
        pass

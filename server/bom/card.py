from server.bom.draw_base import *
from six import string_types

# This should be used for the API
decks = {'french': ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "hj", "hq", "hk",
                    "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "tj", "tq", "tk",
                    "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "cj", "cq", "ck",
                    "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "pj", "pq", "pk"],
         }


class CardDraw(BaseDraw):
    """
    Stores the content of a draw of CardsDraw
    """
    TYPES = BaseDraw.TYPES.copy()
    TYPES['type_of_deck'] = string_types

    def __init__(self, type_of_deck='french', **kwargs):
        super(CardDraw, self).__init__(**kwargs)

        self.type_of_deck = type_of_deck
        """Type of deck to be used"""

    def is_feasible(self):
        if self.type_of_deck not in decks:
            # The selected deck is not available
            return False

        if self.number_of_results < 1:
            # At least one result is requested
            return False

        if self.number_of_results > len(decks[self.type_of_deck]):
            # The selected deck does not have so many cards
            return False

        return True

    def generate_result(self):
        return [random.randint(1, len(decks[self.type_of_deck])) for x in range(0, self.number_of_results)]

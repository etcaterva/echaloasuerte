from server.bom.draw_base import BaseDraw
import random
import logging

def is_power_of_two(num):
    return num and not num & (num - 1)

class TournamentDraw(BaseDraw):
    """
    Stores the content of a draw for a tournament
    """

    def __init__(self, participants=None, **kwargs):
        super(TournamentDraw, self).__init__(**kwargs)

        self.participants = participants if participants else []
        """Participants of the tournament"""

    def generate_result(self):
        source = self.participants[:]
        random.shuffle(source)
        while not is_power_of_two(len(source)):
            source.append("-")
        groups = zip(*(iter(source),) * 2)
        return groups

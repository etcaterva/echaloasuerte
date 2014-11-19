from django.db import models
from django.utils.translation import ugettext_lazy as _
import random


class DiceDraw(models.Model):
    """
    Class that represents a draw with the details choose random items from a list
    """

    number_of_dice = models.PositiveIntegerField(_("Number of dice"), blank=False, null=False, default=1)
    """Number of dice to roll"""

    def is_feasible(self):
        return self.number_of_dice > 0

    def toss(self):
        """Carries out the toss"""
        result = DiceResult()
        result.draw = self
        result.save()

        for i in range(0, self.number_of_dice):
            random_value = random.randint(0, 6)
            number = Die(value=random_value)
            number.result = result
            number.save()
        return result

    class Meta:
        app_label = "server"


class DiceResult(models.Model):
    """
    Class that store a die as the result (or part of it) of a DiceDraw
    Note that one result may be one or several dice
    """

    class Meta:
        app_label = "server"

    draw = models.ForeignKey(DiceDraw, verbose_name=_("Draw"), blank=False, null=False, unique=False,
                             related_name="results")
    """ Stores the draw that generated this result. """

    timestamp = models.DateTimeField(auto_now_add=True)
    """Stores when the result was created."""


class Die(models.Model):
    """
    Class that store the items in the draw
    Note that one result may be one or several items
    """

    class Meta:
        app_label = "server"

    value = models.IntegerField(blank=False, null=False)
    """String the value of the die"""

    result = models.ForeignKey(DiceResult, verbose_name=_("Result"), blank=False, null=False, unique=False,
                               related_name="dice")

    def __str__(self):
        return self.value
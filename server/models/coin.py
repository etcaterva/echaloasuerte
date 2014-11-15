from django.db import models
from django.utils.translation import ugettext_lazy as _
import random


class CoinDraw(models.Model):
    """
    Class that represents a draw with coin (flip a coin)
    """

    def is_feasible(self):
        return True

    def toss(self):
        """Carries out the toss"""
        result = CoinResult()
        result.draw = self
        result.save()

        result.value = random.choice(['head', 'tail'])
        return result

    class Meta:
        app_label = "server"


class CoinResult(models.Model):
    """
    Class that represents a result of a CoinDraw. Value may be "head" or "tail"
    """

    class Meta:
        app_label = "server"

    draw = models.ForeignKey(CoinDraw, verbose_name=_("Draw"), blank=False, null=False, unique=False,
                             related_name="results")
    """ Stores the draw that generated this result. """

    value = models.CharField(max_length=5, blank=False, null=False)


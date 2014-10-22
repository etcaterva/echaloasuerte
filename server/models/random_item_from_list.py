from django.db import models
from django.utils.translation import ugettext_lazy as _

class RandomItemFromListDraw(models.Model):
    """
    Class that represents a draw with the details choose random items from a list
    """

    #TODO Find the best way to store it in a model (Foreign Key, JSON...)
    items = []
    """List which store the items as strings"""

    number_of_results = models.PositiveIntegerField(_("Number of results"), blank=False, null=False, default=1)
    """Number of Random items to choose"""

    allow_repeat = models.BooleanField(_("Allow Repetitions"), blank=False, null=False, default=False)
    """Whether the set of items to generate can contain repetitions."""

    def is_feasible(self):
        return True


class RandomItemFromListResult(models.Model):
    """
    Class that represents a result of a RandomItemFromListDraw. It consist on one or several items from the list
    """
    pass
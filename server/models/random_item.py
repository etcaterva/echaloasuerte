from copy import name
from django.db import models
from django.utils.translation import ugettext_lazy as _


class RandomItemDraw(models.Model):
    """
    Class that represents a draw with the details choose random items from a list
    """

    number_of_results = models.PositiveIntegerField(_("Number of results"), blank=False, null=False, default=1)
    """Number of Random items to choose"""

    allow_repeat = models.BooleanField(_("Allow Repetitions"), blank=False, null=False, default=False)
    """Whether the set of items to generate can contain repetitions."""

    def is_feasible(self):
        if self.draw_results.count() < 1:
            return False
        return self.allow_repeat or self.number_of_results <= self.draw_results.count()

    class Meta:
        app_label="server"


class Item(models.Model):
    """
    Class that store the items in the draw
    Note that one result may be one or several items
    """
    class Meta:
        app_label="server"

    name = models.CharField(max_length=20)
    """String that stores the name of the item"""

    #result = models.ForeignKey(RandomItemResult, verbose_name=_("Result"), blank=False, null=False, unique=False, related_name="result_items")
    """Stores the result asociated with this item"""


class RandomItemResult(models.Model):
    """
    Class that represents a result of a RandomItemDraw. It consist on one or several items from the list
    """
    class Meta:
        app_label="server"

    draw = models.ForeignKey(RandomItemDraw, verbose_name=_("Draw"), blank=False, null=False, unique=False, related_name="draw_results")
    """ Stores the draw that generated this result. """

    items = models.ManyToManyField(Item, blank=False, null=False)


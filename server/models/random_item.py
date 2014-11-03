from copy import name
from django.db import models
from django.utils.translation import ugettext_lazy as _
import random


class Item(models.Model):
    """
    Class that store the items in the draw
    Note that one result may be one or several items
    """

    class Meta:
        app_label = "server"

    name = models.CharField(max_length=20, blank=False, null=False)
    """String that stores the name of the item"""

    def __str__(self):
        return self.name


class RandomItemDraw(models.Model):
    """
    Class that represents a draw with the details choose random items from a list
    """

    number_of_results = models.PositiveIntegerField(_("Number of results"), blank=False, null=False, default=1)
    """Number of Random items to choose"""

    allow_repeat = models.BooleanField(_("Allow Repetitions"), blank=False, null=False, default=False)
    """Whether the set of items to generate can contain repetitions."""

    items = models.ManyToManyField(Item, blank=False, null=False)
    """The available set of item to choose from"""

    def is_feasible(self):
        if self.items.all().count() < 1:
            return False
        return self.allow_repeat or self.number_of_results <= self.items.all().count()

    '''Preconditions: has to be feasible'''

    def toss(self):
        """Carries out the toss"""
        result = RandomItemResult()
        result.draw = self
        result.save()

        value_max = self.items.count() - 1
        options = self.items.order_by("-id")
        for i in range(0, self.number_of_results):
            while True:
                random_value = random.randint(0, value_max)
                random_item = options[random_value]
                if (self.allow_repeat or result.items.filter(id=random_item.id).count() == 0):
                    break
            RandomItemResultItem(result=result, item=random_item).save()

    class Meta:
        app_label = "server"


class RandomItemResult(models.Model):
    """
    Class that represents a result of a RandomItemDraw. It consist on one or several items from the list
    """

    class Meta:
        app_label = "server"

    draw = models.ForeignKey(RandomItemDraw, verbose_name=_("Draw"), blank=False, null=False, unique=False,
                             related_name="results")
    """ Stores the draw that generated this result. """

    items = models.ManyToManyField(Item, through='RandomItemResultItem', blank=False, null=False)
    """ Stores the result set of items """

    timestamp = models.DateTimeField(auto_now_add=True)
    """Stores when the result was created."""


class RandomItemResultItem(models.Model):
    """
    Class that represents the many-to-many relationship between RandomItemResult and Item
    The reason to use a intermediary model is to allow duplicate entries
    """

    class Meta:
        app_label = "server"

    result = models.ForeignKey(RandomItemResult)
    """Foreign Key to the RandomItemResult"""

    item = models.ForeignKey(Item)
    """Foreign Key to the Item"""
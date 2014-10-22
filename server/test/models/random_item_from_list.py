from django.db import models


class RandomItemFromListDraw(models.Model):
    """
    Class that represents a draw with the details choose random items from a list
    """
    pass


class RandomItemFromListResult(models.Model):
    """
    Class that represents a result of a RandomItemFromListDraw. It consist on one or several items from the list
    """
    pass
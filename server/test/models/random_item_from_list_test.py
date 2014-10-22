from django.test import TestCase
from server.models.random_item_from_list import RandomItemFromListDraw


class RandomItemFromListTestCase(TestCase):
    def setUp(self):
        pass

    def build_random_item_from_list_test(self):
        """Builds a draw for 'random item from a list'"""
        RandomItemFromListDraw()
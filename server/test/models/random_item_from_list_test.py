from django.test import TestCase
from server.models.random_item_from_list import RandomItemFromListDraw


class RandomItemFromListTestCase(TestCase):
    def setUp(self):
        pass

    def build_random_item_from_list_test(self):
        """RandomItemFromList: Basic construction"""
        RandomItemFromListDraw()

    def default_constructor_test(self):
        """RandomItemFromList: Default constructor"""
        tested_item = RandomItemFromListDraw()
        self.assertEqual(tested_item.number_of_results,1)
        self.assertEqual(tested_item.allow_repeat,False)

    def parametrized_constructor_test(self):
        """RandomItemFromList: Parametrized constructor"""
        tested_item = RandomItemFromListDraw(allow_repeat=True, number_of_results = 5)
        self.assertEqual(tested_item.number_of_results,5)
        self.assertEqual(tested_item.allow_repeat,True)
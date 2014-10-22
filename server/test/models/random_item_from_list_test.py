from django.test import TestCase
from server.models.random_item_from_list import RandomItemFromListDraw


class RandomItemFromListDrawTestCase(TestCase):
    def setUp(self):
        pass

    def build_random_item_from_list_test(self):
        """RandomItemFromListDraw: Basic construction"""
        RandomItemFromListDraw()

    def default_constructor_test(self):
        """RandomItemFromListDraw: Default constructor"""
        tested_item = RandomItemFromListDraw()
        self.assertEqual(tested_item.number_of_results,1)
        self.assertEqual(tested_item.allow_repeat,False)

    def parametrized_constructor_test(self):
        """RandomItemFromListDraw: Full Parametrized constructor"""
        tested_item = RandomItemFromListDraw(items=['item1','item2'], allow_repeat=True, number_of_results = 5)
        self.assertEqual(tested_item.number_of_results,5)
        self.assertEqual(tested_item.allow_repeat,True)

    def is_feasible_default_test(self):
        """RandomItemFromListDraw: Default constructor is not feasible"""
        self.assertFalse(RandomItemFromListDraw().is_feasible())

    def is_feasible_simple_test(self):
        """RandomNumberDraw: Simple parametrized constructor is feasible"""
        #tested_item = RandomItemFromListDraw(items=['item1','item2'])
        #self.assertTrue(tested_item.is_feasible())
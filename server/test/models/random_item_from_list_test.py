from django.test import TestCase
from server.models import *
import django

class RandomItemFromListDrawTestCase(TestCase):
    def setUp(self):
        django.setup()

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
        tested_item = RandomItemFromListDraw(number_of_results = 5, allow_repeat=True)
        self.assertEqual(tested_item.number_of_results,5)
        self.assertEqual(tested_item.allow_repeat,True)

    def is_feasible_default_test(self):
        """RandomItemFromListDraw: Default constructor is not feasible"""
        self.assertFalse(RandomItemFromListDraw().is_feasible())

    def is_feasible_simple_test(self):
        """RandomNumberDraw: Simple parametrized constructor is feasible"""
        #tested_item = RandomItemFromListDraw(items=['item1','item2'])
        #self.assertTrue(tested_item.is_feasible())

    '''def relationship_draw_result_test(self):
        t_draw = RandomItemFromListDraw()
        t_draw.save()
        t_result1 = RandomItemFromListResult()
        t_result1.draw = t_draw
        t_result2 = RandomItemFromListResult()
        t_result2.draw = t_draw
        self.assertEqual(0, t_draw.draw_results.count())
        t_result1.save()
        self.assertEqual(1, t_draw.draw_results.count())
        t_result2.save()
        self.assertEqual(2, t_draw.draw_results.count())'''


from django.test import TestCase
from server.models import *
import django

class RandomItemFromListDrawTestCase(TestCase):
    def setUp(self):
        django.setup()

    def build_random_item_from_list_test(self):
        """RandomItemDraw: Basic construction"""
        RandomItemDraw()

    def default_constructor_test(self):
        """RandomItemDraw: Default constructor"""
        tested_item = RandomItemDraw()
        self.assertEqual(tested_item.number_of_results,1)
        self.assertEqual(tested_item.allow_repeat,False)

    def parametrized_constructor_test(self):
        """RandomItemDraw: Full Parametrized constructor"""
        tested_item = RandomItemDraw(number_of_results = 5, allow_repeat=True)
        self.assertEqual(tested_item.number_of_results,5)
        self.assertEqual(tested_item.allow_repeat,True)

    def is_feasible_default_test(self):
        """RandomItemDraw: Default constructor is not feasible"""
        self.assertFalse(RandomItemDraw().is_feasible())

    def is_feasible_simple_test(self):
        """RandomNumberDraw: Simple parametrized constructor is feasible"""
        #tested_item = RandomItemDraw(items=['item1','item2'])
        #self.assertTrue(tested_item.is_feasible())

    '''def relationship_draw_result_test(self):
        t_draw = RandomItemDraw()
        t_draw.save()
        t_result1 = RandomItemResult()
        t_result1.draw = t_draw
        t_result2 = RandomItemResult()
        t_result2.draw = t_draw
        self.assertEqual(0, t_draw.draw_results.count())
        t_result1.save()
        self.assertEqual(1, t_draw.draw_results.count())
        t_result2.save()
        self.assertEqual(2, t_draw.draw_results.count())'''


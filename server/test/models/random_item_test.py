from django.test import TestCase
from server.models import *
import django

class RandomItemDrawTestCase(TestCase):
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
        t_draw = RandomItemDraw()
        t_draw.save()
        self.assertFalse(t_draw.is_feasible())

    def is_feasible_simple_test(self):
        """RandomNumberDraw: Simple parametrized constructor is feasible"""
        #TODO fix this
        t_draw = RandomItemDraw()
        t_draw.save()
        t_item = Item(name="item1")
        t_item.save()
        t_draw.items.add(t_item)
        self.assertTrue(t_draw.is_feasible())

    def relationship_draw_result_test(self):
        """RandomNumberDraw: Relationship Draw-Result"""
        t_draw = RandomItemDraw()
        t_draw.save()
        t_result1 = RandomItemResult()
        t_result1.draw = t_draw
        t_result2 = RandomItemResult()
        t_result2.draw = t_draw
        self.assertEqual(0, t_draw.results.count())
        t_result1.save()
        self.assertEqual(1, t_draw.results.count())
        t_result2.save()
        self.assertEqual(2, t_draw.results.count())


    def relationship_result_item_test(self):
        """RandomNumberDraw: Relationship Result-Item"""
        t_draw = RandomItemDraw()
        t_draw.save()
        t_result = RandomItemResult()
        t_result.draw = t_draw
        t_result.save()

        t_item1 = Item(name="item1")
        t_item1.save()
        t_item2 = Item(name="item2")
        t_item2.save()
        self.assertEqual(0, t_result.items.filter(name="item2").count())
        t_result.items.add(t_item1)
        self.assertEqual(0, t_result.items.filter(name="item2").count())
        t_result.items.add(t_item2)
        self.assertEqual(1, t_result.items.filter(name="item2").count())
        self.assertEqual(2, t_result.items.all().count())


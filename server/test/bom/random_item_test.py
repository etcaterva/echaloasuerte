from django.test import TestCase
from server.bom.random_item import *

class RandomItemDrawTest(TestCase):
    """ Basic sanity test for mongodb driver"""
    def setUp(self):
        self.dummy_draw = RandomItemDraw()

    def default_constructor_test(self):
        """RandomItemDraw: Basic construction"""
        pass

    def serialization_test(self):
        """RandomItemDraw: Serialization"""
        raw = RandomItemDraw(items=[1,2]).__dict__
        self.assertEqual(raw["items"],[1,2])

    def deserialization_test(self):
        """RandomItemDraw: Deserialization"""
        raw = {"number_of_results":2,"items":[1,2,3]}
        item = RandomItemDraw(**raw)
        self.assertEqual(item.number_of_results,2)
        self.assertEqual(item.items,[1,2,3])

    def is_feasible_test(self):
        """RandomItemDraw: Is Feasible"""
        self.assertFalse(RandomItemDraw().is_feasible())

    def is_feasible_simple_test(self):
        """RandomItemDraw: Simple parametrized constructor is feasible"""
        tested_item = RandomItemDraw(items=[1,2])
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_range_and_results_ok_test(self):
        """RandomItemDraw: Tight draw results is feasible"""
        tested_item = RandomItemDraw(items=[1,2,3], number_of_results=3, allow_repeat=False)
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_too_many_results_ko_test(self):
        """RandomItemDraw: Too many results requested is not feasible"""
        tested_item = RandomItemDraw(items=[1,2,3], number_of_results=4, allow_repeat=False)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_many_results_with_repeat_ok_test(self):
        """RandomItemDraw: Many results requested with repeat is feasible"""
        tested_item = RandomItemDraw(items=["A"], number_of_results=4, allow_repeat=True)
        self.assertTrue(tested_item.is_feasible())

    def toss_once_test(self):
        """RandomItemDraw: Toss once"""
        tested_item = RandomItemDraw(items=["A"])
        self.assertEqual(0,len(tested_item.results))
        self.assertEqual("A",tested_item.toss()["items"][0])
        self.assertEqual(1,len(tested_item.results))
        self.assertEqual(1,len(tested_item.results[0]["items"]))

    def toss_same_twice_test(self):
        """RandomItemDraw: Toss same twice"""
        tested_item2 = RandomItemDraw(items=[0])
        self.assertEqual(0,len(tested_item2.results))
        self.assertEqual(0,tested_item2.toss()["items"][0])
        self.assertEqual(0,tested_item2.toss()["items"][0])
        self.assertEqual(2,len(tested_item2.results))
        self.assertEqual(1,len(tested_item2.results[0]["items"]))
        self.assertEqual(1,len(tested_item2.results[1]["items"]))

    def toss_two_items_test(self):
        """RandomItemDraw: Toss generate two items"""
        tested_item2 = RandomItemDraw(items=[0], number_of_results=2,allow_repeat=True, results = [])
        self.assertEqual(0,len(tested_item2.results))
        self.assertEqual(0,tested_item2.toss()["items"][0])
        self.assertEqual(1,len(tested_item2.results))
        self.assertEqual(2,len(tested_item2.results[0]["items"]))

    def toss_on_existing_test(self):
        """RandomItemDraw: Toss when list created with results already"""
        tested_item2 = RandomItemDraw(items=[0], number_of_results=2,allow_repeat=True,results=[{"items":[0]}])
        self.assertEqual(1,len(tested_item2.results))
        self.assertEqual(0,tested_item2.toss()["items"][0])
        self.assertEqual(2,len(tested_item2.results))

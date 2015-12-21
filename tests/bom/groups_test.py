from django.test import TestCase

from server.bom.group import *


class GroupDrawTest(TestCase):
    """ Basic sanity test for mongodb driver"""

    def setUp(self):
        self.dummy_draw = GroupsDraw()

    def default_constructor_test(self):
        """GroupsDraw: Basic construction"""
        pass

    def serialization_test(self):
        """GroupsDraw: Serialization"""
        raw = GroupsDraw(items=[1, 2]).__dict__
        self.assertEqual(raw["items"], [1, 2])

    def deserialization_test(self):
        """GroupsDraw: Deserialization"""
        raw = {"number_of_results": 2, "items": [1, 2, 3]}
        item = GroupsDraw(**raw)
        self.assertEqual(item.number_of_results, 2)
        self.assertEqual(item.items, [1, 2, 3])

    def is_feasible_test(self):
        """GroupsDraw: Is Feasible"""
        self.assertFalse(GroupsDraw().is_feasible())

    def is_feasible_simple_test(self):
        """GroupsDraw: Simple parametrized constructor is feasible"""
        tested_item = GroupsDraw(items=[1, 2])
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_range_and_results_ok_test(self):
        """GroupsDraw: Tight draw results is feasible"""
        tested_item = GroupsDraw(items=[1, 2, 3], number_of_results=3)
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_not_enought_results_ko_test(self):
        """GroupsDraw: Number of results requested less than one is not feasible"""
        tested_item = GroupsDraw(items=[1, 2, 3], number_of_results=0)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_results_over_the_limit_ko_test(self):
        """GroupsDraw: Too many results requested (over the limit) is not feasible"""
        tested_item = GroupsDraw(items=[1, 2, 3], number_of_results=100)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_too_many_results_ko_test(self):
        """GroupsDraw: Too many results requested is not feasible"""
        tested_item = GroupsDraw(items=[1, 2, 3], number_of_results=4)
        self.assertFalse(tested_item.is_feasible())

    def toss_once_test(self):
        """GroupsDraw: Toss once"""
        tested_item = GroupsDraw(items=["A"])
        self.assertEqual(0, len(tested_item.results))
        self.assertEqual(["A"], tested_item.toss()["items"][0])
        self.assertEqual(1, len(tested_item.results))
        self.assertEqual(1, len(tested_item.results[0]["items"]))

    def toss_same_twice_test(self):
        """GroupsDraw: Toss same twice"""
        tested_item2 = GroupsDraw(items=[0])
        self.assertEqual(0, len(tested_item2.results))
        self.assertEqual([0], tested_item2.toss()["items"][0])
        self.assertEqual([0], tested_item2.toss()["items"][0])
        self.assertEqual(2, len(tested_item2.results))
        self.assertEqual(1, len(tested_item2.results[0]["items"]))
        self.assertEqual(1, len(tested_item2.results[1]["items"]))

    def toss_two_items_test(self):
        """GroupsDraw: Toss generate two items"""
        tested_item2 = GroupsDraw(items=[0], number_of_results=2, results=[])
        self.assertEqual(0, len(tested_item2.results))
        self.assertEqual([0], tested_item2.toss()["items"][0])
        self.assertEqual(1, len(tested_item2.results))
        self.assertEqual(2, len(tested_item2.results[0]["items"]))

    def toss_on_existing_test(self):
        """GroupsDraw: Toss when list created with results already"""
        tested_item2 = GroupsDraw(items=[0], number_of_results=2, results=[{"items": [0]}])
        self.assertEqual(1, len(tested_item2.results))
        self.assertEqual([0], tested_item2.toss()["items"][0])
        self.assertEqual(2, len(tested_item2.results))

    def toss_multiple_items_test(self):
        tested_item2 = GroupsDraw(items=list(range(5)), number_of_results=2)
        result = tested_item2.toss()["items"]
        self.assertEqual(2, len(result))
        for item in list(range(5)):
            self.assertEqual(1, sum([res.count(item) for res in result]))

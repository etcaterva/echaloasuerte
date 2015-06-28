from django.test import TestCase
from server.bom.random_number import *


class RandomNumberDrawTest(TestCase):
    """ Basic sanity test for mongodb driver"""

    def setUp(self):
        self.dummy_draw = RandomNumberDraw()

    def default_constructor_test(self):
        """RandomNumberDraw: Basic construction"""
        pass

    def serialization_test(self):
        """RandomNumberDraw: Serialization"""
        raw = RandomNumberDraw(range_min=0).__dict__
        self.assertEqual(raw["range_min"], 0)

    def deserialization_test(self):
        """RandomNumberDraw: Deserialization"""
        raw = {"range_min": 5, "range_max": 10}
        item = RandomNumberDraw(**raw)
        self.assertEqual(item.range_min, 5)
        self.assertEqual(item.range_max, 10)

    def is_feasible_test(self):
        """RandomNumberDraw: Is Feasible"""
        self.assertTrue(RandomNumberDraw().is_feasible())

    def is_feasible_simple_test(self):
        """RandomNumberDraw: Simple parametrized constructor is feasible"""
        tested_item = RandomNumberDraw(range_max=5)
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_range_and_results_ok_test(self):
        """RandomNumberDraw: Acceptable range and number of results is feasible"""
        tested_item = RandomNumberDraw(range_min=2, range_max=5, number_of_results=3, allow_repeat=False)
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_range_ko_test(self):
        """RandomNumberDraw: Range requested is not feasible"""
        tested_item = RandomNumberDraw(range_max=2, range_min=4)
        self.assertFalse(tested_item.is_feasible())

    def audits_are_added_test(self):
        """RandomNumberDraw: Range requested is not feasible"""
        tested_item = RandomNumberDraw(range_max=2, range_min=4)
        self.assertFalse(tested_item.audit)
        tested_item.add_audit("Something changed")
        self.assertTrue(tested_item.audit)

    def is_feasible_not_enough_results_ko_test(self):
        """RandomNumberDraw: Number of numbers requested less than one is not feasible"""
        tested_item = RandomNumberDraw(range_min=2, range_max=5, number_of_results=0, allow_repeat=False)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_too_many_results_ko_test(self):
        """RandomNumberDraw: Too many results requested is not feasible"""
        tested_item = RandomNumberDraw(range_min=2, range_max=5, number_of_results=4, allow_repeat=False)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_results_over_the_limit_ko_test(self):
        """RandomNumberDraw: Too many results requested is not feasible"""
        tested_item = RandomNumberDraw(range_min=2, range_max=5, number_of_results=60, allow_repeat=True)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_many_results_with_repeat_ok_test(self):
        """RandomNumberDraw: Many results requested with repeat is feasible"""
        tested_item = RandomNumberDraw(range_max=5, range_min=2, number_of_results=4, allow_repeat=True)
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_range_with_repeat_ko_test(self):
        """RandomNumberDraw: Invalid range requested with repeat is not feasible"""
        tested_item = RandomNumberDraw(range_max=2, range_min=4, allow_repeat=True)
        self.assertFalse(tested_item.is_feasible())

    def toss_once_test(self):
        """RandomNumberDraw: Toss once"""
        tested_item = RandomNumberDraw(range_max=0, range_min=0)
        self.assertEqual(0, len(tested_item.results))
        self.assertEqual(0, tested_item.toss()["items"][0])
        self.assertEqual(1, len(tested_item.results))
        self.assertEqual(1, len(tested_item.results[0]["items"]))

    def toss_same_twice_test(self):
        """RandomNumberDraw: Toss same twice"""
        tested_item2 = RandomNumberDraw(range_max=0, range_min=0)
        self.assertEqual(0, len(tested_item2.results))
        self.assertEqual(0, tested_item2.toss()["items"][0])
        self.assertEqual(0, tested_item2.toss()["items"][0])
        self.assertEqual(2, len(tested_item2.results))
        self.assertEqual(1, len(tested_item2.results[0]["items"]))
        self.assertEqual(1, len(tested_item2.results[1]["items"]))

    def toss_two_items_test(self):
        """RandomNumberDraw: Toss generate two items"""
        tested_item2 = RandomNumberDraw(range_max=0, range_min=0, number_of_results=2, allow_repeat=True)
        self.assertEqual(0, len(tested_item2.results))
        self.assertEqual(0, tested_item2.toss()["items"][0])
        self.assertEqual(1, len(tested_item2.results))
        self.assertEqual(2, len(tested_item2.results[0]["items"]))

    def toss_on_existing_test(self):
        """RandomNumberDraw: Toss when list created with results already"""
        tested_item2 = RandomNumberDraw(range_max=0, range_min=0, number_of_results=2, allow_repeat=True,
                                        results=[{"items": [0]}])
        self.assertEqual(1, len(tested_item2.results))
        self.assertEqual(0, tested_item2.toss()["items"][0])
        self.assertEqual(2, len(tested_item2.results))

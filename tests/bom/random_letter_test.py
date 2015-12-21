import string

from django.test import TestCase

from server.bom.random_letter import *


class RandomLetterDrawTest(TestCase):
    """ Basic sanity test for mongodb driver"""

    def setUp(self):
        self.dummy_draw = RandomLetterDraw()

    def default_constructor_test(self):
        """RandomLetterDraw: Basic construction"""
        pass

    def serialization_test(self):
        """RandomLetterDraw: Serialization"""
        raw = RandomLetterDraw().__dict__
        self.assertEqual(raw["number_of_results"], 1)

    def deserialization_test(self):
        """RandomLetterDraw: Deserialization"""
        raw = {"number_of_results": 5}
        item = RandomLetterDraw(**raw)
        self.assertEqual(item.number_of_results, 5)

    def is_feasible_test(self):
        """RandomLetterDraw: Is Feasible"""
        self.assertTrue(RandomLetterDraw().is_feasible())

    def is_feasible_range_and_results_ok_test(self):
        """RandomLetterDraw: Acceptable range and number of results is feasible"""
        tested_item = RandomLetterDraw(number_of_results=3)
        self.assertTrue(tested_item.is_feasible())

    def audits_are_added_test(self):
        """RandomLetterDraw: Range requested is not feasible"""
        tested_item = RandomLetterDraw()
        self.assertFalse(tested_item.audit)
        tested_item.add_audit("Something changed")
        self.assertTrue(tested_item.audit)

    def is_feasible_not_enough_results_ko_test(self):
        """RandomLetterDraw: Letter of numbers requested less than one is not feasible"""
        tested_item = RandomLetterDraw(number_of_results=0)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_results_over_the_limit_ko_test(self):
        """RandomLetterDraw: Too many results requested is not feasible"""
        tested_item = RandomLetterDraw(number_of_results=60)
        self.assertFalse(tested_item.is_feasible())

    def toss_once_test(self):
        """RandomLetterDraw: Toss once"""
        tested_item = RandomLetterDraw()
        self.assertEqual(0, len(tested_item.results))
        self.assertTrue(tested_item.toss()["items"][0] in string.ascii_letters)
        self.assertEqual(1, len(tested_item.results))
        self.assertEqual(1, len(tested_item.results[0]["items"]))

    def toss_same_twice_test(self):
        """RandomLetterDraw: Toss same twice"""
        tested_item2 = RandomLetterDraw()
        self.assertEqual(0, len(tested_item2.results))
        self.assertTrue(tested_item2.toss()["items"][0] in string.ascii_letters)
        self.assertTrue(tested_item2.toss()["items"][0] in string.ascii_letters)
        self.assertEqual(2, len(tested_item2.results))
        self.assertEqual(1, len(tested_item2.results[0]["items"]))
        self.assertEqual(1, len(tested_item2.results[1]["items"]))

    def toss_two_items_test(self):
        """RandomLetterDraw: Toss generate two items"""
        tested_item2 = RandomLetterDraw(number_of_results=2)
        self.assertEqual(0, len(tested_item2.results))
        self.assertTrue(tested_item2.toss()["items"][0] in string.ascii_letters)
        self.assertEqual(1, len(tested_item2.results))
        self.assertEqual(2, len(tested_item2.results[0]["items"]))

    def toss_on_existing_test(self):
        """RandomLetterDraw: Toss when list created with results already"""
        tested_item2 = RandomLetterDraw(number_of_results=2, results=[{"items": ['a']}])
        self.assertEqual(1, len(tested_item2.results))
        self.assertTrue(tested_item2.toss()["items"][0] in string.ascii_letters)
        self.assertEqual(2, len(tested_item2.results))

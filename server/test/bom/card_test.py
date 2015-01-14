from django.test import TestCase
from server.bom.card import *

class DiceDrawTest(TestCase):
    """ Basic sanity test for mongodb driver"""
    def setUp(self):
        self.dummy_draw = CardDraw()

    def default_constructor_test(self):
        """CardDraw: Basic construction"""
        pass

    def serialization_test(self):
        """CardDraw: Serialization"""
        raw = CardDraw(number_of_results=1).__dict__
        self.assertEqual(raw["number_of_results"], 1)

    def deserialization_test(self):
        """CardDraw: Deserialization"""
        raw = {"number_of_results": 2}
        item = CardDraw(**raw)
        self.assertEqual(item.number_of_results, 2)

    def is_feasible_test(self):
        """CardDraw: Is Feasible"""
        self.assertTrue(CardDraw().is_feasible())
        self.assertFalse(CardDraw(number_of_results=500).is_feasible())

    def toss_once_test(self):
        """CardDraw: Toss once"""
        tested_item = CardDraw()
        self.assertEqual(0, len(tested_item.results))
        tested_item.toss()
        self.assertEqual(1, len(tested_item.results))

    def toss_same_twice_test(self):
        """CardDraw: Toss same twice"""
        tested_item2 = CardDraw()
        self.assertEqual(0, len(tested_item2.results))
        tested_item2.toss()
        tested_item2.toss()
        self.assertEqual(2, len(tested_item2.results))
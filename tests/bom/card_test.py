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
        raw = CardDraw(number_of_results=1, type_of_deck="french").__dict__
        self.assertEqual(raw["number_of_results"], 1)

    def deserialization_test(self):
        """CardDraw: Deserialization"""
        raw = {"number_of_results": 2}
        item = CardDraw(**raw)
        self.assertEqual(item.number_of_results, 2)

    def is_feasible_default_ok_test(self):
        """CardDraw: Default draw is feasible"""
        self.assertTrue(CardDraw().is_feasible())

    def is_feasible_parametrized_ok_test(self):
        """CardDraw: parametrized draw is feasible"""
        tested_item = CardDraw(number_of_results=5, type_of_deck="french")
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_not_enough_results_ko_test(self):
        """CardDraw: Number of cards requested less than one is not feasible"""
        tested_item = CardDraw(number_of_results=0)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_too_many_results_ko_test(self):
        """CardDraw: More cards requested than the deck has is not feasible"""
        tested_item = CardDraw(type_of_deck="french", number_of_results=60)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_deck_not_found_ko_test(self):
        """CardDraw: Invalid type of deck is not feasible"""
        tested_item = CardDraw(number_of_results=5,
                               type_of_deck="what are you doing here?")
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_not_enough_results_ko_test(self):
        """CardDraw: The deck requested has to be available"""
        tested_item = CardDraw(number_of_results=0)
        self.assertFalse(tested_item.is_feasible())

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
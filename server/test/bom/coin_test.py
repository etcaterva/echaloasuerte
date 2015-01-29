from django.test import TestCase
from server.bom.coin import *


class CoinDrawTest(TestCase):
    """ Basic sanity test for mongodb driver"""

    def setUp(self):
        self.dummy_draw = CoinDraw()

    def default_constructor_test(self):
        """CoinDraw: Basic construction"""
        pass

    def serialization_test(self):
        """CoinDraw: Serialization"""
        raw = CoinDraw(number_of_results=1).__dict__
        self.assertEqual(raw["number_of_results"], 1)

    def deserialization_test(self):
        """CoinDraw: Deserialization"""
        raw = {"number_of_results": 1}
        item = CoinDraw(**raw)
        self.assertEqual(item.number_of_results, 1)

    def is_feasible_default_test(self):
        """CoinDraw: Default constructor Is Feasible"""
        self.assertTrue(CoinDraw().is_feasible())

    def is_feasible_parametrized_test(self):
        """CoinDraw: Parametrized constructor Is Feasible"""
        tested_item = CoinDraw(number_of_results=3)
        self.assertTrue(tested_item.is_feasible())

    def if_feasible_too_many_results_ko_test(self):
        """CoinDraw: Too many results is not feasible"""
        tested_item = CoinDraw(number_of_results=30)
        self.assertFalse(tested_item.is_feasible())

    def toss_once_test(self):
        """CoinDraw: Toss once"""
        tested_item = CoinDraw()
        self.assertEqual(0, len(tested_item.results))
        tested_item.toss()
        self.assertEqual(1, len(tested_item.results))

    def toss_same_twice_test(self):
        """CoinDraw: Toss same twice"""
        tested_item2 = CoinDraw()
        self.assertEqual(0, len(tested_item2.results))
        tested_item2.toss()
        tested_item2.toss()
        self.assertEqual(2, len(tested_item2.results))

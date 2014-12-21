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
        self.assertEqual(raw["number_of_results"],1)

    def deserialization_test(self):
        """CoinDraw: Deserialization"""
        raw = {"number_of_results":2}
        item = CoinDraw(**raw)
        self.assertEqual(item.number_of_results,2)

    def is_feasible_test(self):
        """CoinDraw: Is Feasible"""
        self.assertTrue(CoinDraw().is_feasible())
        self.assertTrue(CoinDraw(number_of_results=500).is_feasible())

    def toss_once_test(self):
        """CoinDraw: Toss once"""
        tested_item = CoinDraw()
        self.assertEqual(0,len(tested_item.results))
        tested_item.toss()
        self.assertEqual(1,len(tested_item.results))

    def toss_same_twice_test(self):
        """CoinDraw: Toss same twice"""
        tested_item2 = CoinDraw()
        self.assertEqual(0,len(tested_item2.results))
        tested_item2.toss()
        tested_item2.toss()
        self.assertEqual(2,len(tested_item2.results))

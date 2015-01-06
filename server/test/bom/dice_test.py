from django.test import TestCase
from server.bom.dice import *

class DiceDrawTest(TestCase):
    """ Basic sanity test for mongodb driver"""
    def setUp(self):
        self.dummy_draw = DiceDraw()

    def default_constructor_test(self):
        """DiceDraw: Basic construction"""
        pass

    def serialization_test(self):
        """DiceDraw: Serialization"""
        raw = DiceDraw(number_of_results=1).__dict__
        self.assertEqual(raw["number_of_results"],1)

    def deserialization_test(self):
        """DiceDraw: Deserialization"""
        raw = {"number_of_results":2}
        item = DiceDraw(**raw)
        self.assertEqual(item.number_of_results,2)

    def is_feasible_test(self):
        """DiceDraw: Is Feasible"""
        self.assertTrue(DiceDraw().is_feasible())
        self.assertTrue(DiceDraw(number_of_results=500).is_feasible())

    def toss_once_test(self):
        """DiceDraw: Toss once"""
        tested_item = DiceDraw()
        self.assertEqual(0,len(tested_item.results))
        tested_item.toss()
        self.assertEqual(1,len(tested_item.results))

    def toss_same_twice_test(self):
        """DiceDraw: Toss same twice"""
        tested_item2 = DiceDraw()
        self.assertEqual(0,len(tested_item2.results))
        tested_item2.toss()
        tested_item2.toss()
        self.assertEqual(2,len(tested_item2.results))

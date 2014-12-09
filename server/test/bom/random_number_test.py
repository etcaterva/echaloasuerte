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
        self.assertEqual(raw["range_min"],0)

    def deserialization_test(self):
        """RandomNumberDraw: Deserialization"""
        raw = {"range_min":5,"range_max":10}
        item = RandomNumberDraw(**raw)
        self.assertEqual(item.range_min,5)
        self.assertEqual(item.range_max,10)


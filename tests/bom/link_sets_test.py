from django.test import TestCase

from server.bom.link_sets import *


class LinkSetsDrawTest(TestCase):
    """ Basic sanity test for linking draws"""

    def setUp(self):
        self.dummy_draw = LinkSetsDraw()

    def default_constructor_test(self):
        """LinkSetsDraw: Basic construction"""
        pass

    def serialization_test(self):
        """LinkSetsDraw: Serialization"""
        raw = LinkSetsDraw(sets=[[1, 2], ['a', 'b']]).__dict__
        self.assertEqual(raw["sets"][0], [1, 2])

    def deserialization_test(self):
        """LinkSetsDraw: Deserialization"""
        raw = {"sets": [[1, 2], ['a', 'b']]}
        item = LinkSetsDraw(**raw)
        self.assertEqual(len(item.sets), 2)

    def is_feasible_test(self):
        """LinkSetsDraw: Is Feasible"""
        self.assertFalse(LinkSetsDraw().is_feasible())

    def is_feasible_simple_test(self):
        """LinkSetsDraw: Simple parametrized constructor is feasible"""
        tested_item = LinkSetsDraw(sets=[[1], [2]])
        self.assertTrue(tested_item.is_feasible())

    def toss_once_test(self):
        """LinkSetsDraw: Toss once"""
        tested_item = LinkSetsDraw(sets=[[1, 2], ['a', 'b']])
        self.assertEqual(0, len(tested_item.results))
        tested_item.toss()
        self.assertEqual(1, len(tested_item.results))
        self.assertEqual(2, len(tested_item.results[0]["items"]))
        self.assertTrue(
            1 in [tested_item.results[0]["items"][0][0], tested_item.results[0]["items"][1][0]])
        self.assertTrue(
            2 in [tested_item.results[0]["items"][0][0], tested_item.results[0]["items"][1][0]])

        self.assertTrue(
            'a' in [tested_item.results[0]["items"][0][1], tested_item.results[0]["items"][1][1]])
        self.assertTrue(
            'b' in [tested_item.results[0]["items"][0][1], tested_item.results[0]["items"][1][1]])


    def toss_same_twice_test(self):
        """LinkSetsDraw: Toss same twice"""
        tested_item2 = LinkSetsDraw(sets=[[1, 2], ['a', 'b']])
        self.assertEqual(0, len(tested_item2.results))
        tested_item2.toss()
        tested_item2.toss()
        self.assertEqual(2, len(tested_item2.results))
        self.assertEqual(2, len(tested_item2.results[0]["items"]))
        self.assertEqual(2, len(tested_item2.results[1]["items"]))
        self.assertEqual(2, len(tested_item2.results[0]["items"][0]))

    def toss_three_items_test(self):
        """LinkSetsDraw: Toss with 3 sets"""
        tested_item2 = LinkSetsDraw(sets=[[1, 2], ['a', 'b'], ['Z', 'Y']])
        self.assertEqual(0, len(tested_item2.results))
        tested_item2.toss()
        self.assertEqual(1, len(tested_item2.results))
        self.assertEqual(3, len(tested_item2.results[0]["items"][0]))

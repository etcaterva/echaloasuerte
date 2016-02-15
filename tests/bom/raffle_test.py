from django.test import TestCase

from server.bom.raffle import *


class RaffleDrawTest(TestCase):
    def setUp(self):
        self.dummy_draw = RaffleDraw()

    def default_constructor_test(self):
        """RaffleDraw: Basic construction"""
        pass

    def serialization_test(self):
        """RaffleDraw: Serialization"""
        raw = RaffleDraw(prices=['price1', 'price2'], registration_type=RaffleDraw.RESTRICTED).__dict__
        self.assertEqual(raw["prices"], ['price1', 'price2'])
        self.assertEqual(raw["registration_type"], RaffleDraw.RESTRICTED)

    def deserialization_test(self):
        """RaffleDraw: Deserialization"""
        raw = {"prices": ['price1', 'price2']}
        item = RaffleDraw(**raw)
        self.assertEqual(item.prices, ['price1', 'price2'])

    def is_feasible_test(self):
        """RaffleDraw: Is Feasible"""
        self.assertFalse(RaffleDraw().is_feasible())

    def is_feasible_restricted_no_participants_test(self):
        """RaffleDraw: Simple parametrized constructor is feasible"""
        tested_item = RaffleDraw(prices=['price1', 'price2'], registration_type=RaffleDraw.RESTRICTED)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_fb_no_participants_test(self):
        """RaffleDraw: Simple parametrized constructor is feasible"""
        tested_item = RaffleDraw(prices=['price1', 'price2'], registration_type=RaffleDraw.FACEBOOK)
        self.assertFalse(tested_item.is_feasible())

    def is_feasible_restricted_test(self):
        """RaffleDraw: Simple parametrized constructor is feasible"""
        tested_item = RaffleDraw(prices=['price1', 'price2'],
                                 registration_type=RaffleDraw.RESTRICTED,
                                 participants=[Participant('id1', 'Julio Iglesias')])
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_fb_test(self):
        """RaffleDraw: Simple parametrized constructor is feasible"""
        tested_item = RaffleDraw(prices=['price1', 'price2'],
                                 registration_type=RaffleDraw.FACEBOOK,
                                 participants=[Participant('id1', 'Paquito the chocolatemaker')])
        self.assertTrue(tested_item.is_feasible())

    def toss_once_test(self):
        """RaffleDraw: Toss once"""
        leonardo = Participant('id1', 'L. Dicaprio')
        tested_item = RaffleDraw(prices=['any oscar'],
                                 registration_type=RaffleDraw.RESTRICTED,
                                 participants=[leonardo])
        self.assertEqual(0, len(tested_item.results))
        self.assertEqual(("any oscar", leonardo), tested_item.toss()["items"][0])
        self.assertEqual(1, len(tested_item.results))
        self.assertEqual(1, len(tested_item.results[0]["items"]))

    def toss_same_twice_test(self):
        """RaffleDraw: Toss same twice"""
        leonardo = Participant('id1', 'L. Dicaprio')
        tested_item = RaffleDraw(prices=['any oscar'],
                                 registration_type=RaffleDraw.RESTRICTED,
                                 participants=[leonardo])
        self.assertEqual(0, len(tested_item.results))
        self.assertEqual(("any oscar", leonardo), tested_item.toss()["items"][0])
        self.assertEqual(("any oscar", leonardo), tested_item.toss()["items"][0])
        self.assertEqual(2, len(tested_item.results))
        self.assertEqual(1, len(tested_item.results[0]["items"]))
        self.assertEqual(1, len(tested_item.results[1]["items"]))



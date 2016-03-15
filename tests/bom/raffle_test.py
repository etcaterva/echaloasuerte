import datetime
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

    def participant_string_test(self):
        """RaffleDraw: From a real issue"""
        draw_init_values = {u'audit': [{u'type': u'DRAW_PARAMETERS', u'datetime': datetime.datetime(2016, 3, 15, 20, 15, 39, 264000)}], u'last_updated': datetime.datetime(2016, 3, 15, 20, 15, 14, 470000), u'is_shared': True, u'number_of_results': 1, u'enable_chat': True, u'description': u'', u'title': u'HAPPY PUNTOS 15/03/2016', u'creation_time': datetime.datetime(2016, 3, 15, 17, 48, 11, 107000), u'results': [{u'publication_datetime': datetime.datetime(2016, 3, 15, 21, 0), u'datetime': datetime.datetime(2016, 3, 15, 17, 48, 35, 628000)}], u'last_updated_time': datetime.datetime(2016, 3, 15, 20, 15, 39, 264000), u'owner': u'kevinbcb1@hotmail.com', u'participants': [u'{1150140965026513:Raquel Edith Farias}', u' {10206101367908306:Claudia Vilchez}', u' {1680310288910569:Marina Pascual Moya}', u' {499746643546169:Ainhoa Valderrey Sanz}', u' {10209337210530208:Alejandra Rosales}', u' {1332864560073478:Amparo Vila Atienza}', u' {1547261422239576:Laura Sanz Castro}', u' {10207923176292508:Denisse Torres}', u' {780063968761469:Raquel Sanz Castro}', u' {1263545430328087:Carmen Carpio}', u' {899349510186364:Gladys Duque Valencia}', u' {10209225469940429:Puri Marti}', u' {10204518596203823:Beatriz Montero Blazquez}', u' {1072844839439784:Lourdes Rodriguez}', u' {10205951582251880:Trinidad Arboleda Caja}', u' {1039065036135462:Ruami Romero}', u' {409748292558464:Marisa Paredes}', u' {1027644373967953:Marys Alvarez}', u' {1122329714486109:Charo del Aguila}', u' {1561798227453199:Felipe Araya Mu\xf1oz}', u' {1047513871961882:Lourdes Loaiza}'], u'registration_requirement': u'login', u'prices': [u'20 Happy Puntos', u' 20 Happy Puntos', u' 20 Happy Puntos'], u'registration_type': u'facebook', u'_id': '56e84adb741c1f777a334d52', u'draw_type': u'raffle', u'users': []}
        draw = RaffleDraw(**draw_init_values)

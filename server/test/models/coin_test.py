from django.test import TestCase
from server.models import *
import django


class CoinDrawTestCase(TestCase):
    def setUp(self):
        django.setup()

    def build_coin_test(self):
        """CoinDraw: Basic construction"""
        CoinDraw()

    def is_feasible_default_test(self):
        """CoinDraw: Default constructor is feasible"""
        t_draw = CoinDraw()
        t_draw.save()
        self.assertTrue(t_draw.is_feasible())

    def relationship_draw_result_test(self):
        """CoinDraw: Relationship Draw-Result"""
        t_draw = CoinDraw()
        t_draw.save()
        t_result1 = CoinResult()
        t_result1.draw = t_draw
        t_result2 = CoinResult()
        t_result2.draw = t_draw
        self.assertEqual(0, t_draw.results.count())
        t_result1.save()
        self.assertEqual(1, t_draw.results.count())
        t_result2.save()
        self.assertEqual(2, t_draw.results.count())

    def toss_one_result_test(self):
        """CoinDraw: Each toss generates a new result"""
        t_draw = CoinDraw()
        t_draw.save()

        self.assertEqual(0, t_draw.results.count())
        t_draw.toss()
        self.assertEqual(1, t_draw.results.count())
        t_draw.toss()
        self.assertEqual(2, t_draw.results.count())

    def different_draws_generate_different_results_test(self):
        """CoinDraw: Different draws generate different results"""
        t_draw1 = CoinDraw()
        t_draw1.save()
        t_draw2 = CoinDraw()
        t_draw2.save()

        self.assertEqual(0, t_draw1.results.count())
        self.assertEqual(0, t_draw2.results.count())
        t_draw1.toss()
        self.assertEqual(1, t_draw1.results.count())
        self.assertEqual(0, t_draw2.results.count())
        t_draw2.toss()
        self.assertEqual(1, t_draw1.results.count())
        self.assertEqual(1, t_draw2.results.count())

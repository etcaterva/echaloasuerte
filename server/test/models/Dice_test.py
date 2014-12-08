from django.test import TestCase
from server.models import *
import django


class DiceTestCase(TestCase):
    def setUp(self):
        django.setup()

    def build_dice_test(self):
        """DiceDraw: Basic construction"""
        DiceDraw()

    def default_constructor_test(self):
        """DiceDraw: Default constructor"""
        tested_item = DiceDraw()
        self.assertEqual(tested_item.number_of_dice, 1)

    def parametrized_constructor_test(self):
        """DiceDraw: Full parametrized constructor"""
        tested_item = DiceDraw(number_of_dice=5)
        self.assertEqual(tested_item.number_of_dice, 5)

    def is_feasible_default_test(self):
        """DiceDraw: Default constructor is feasible"""
        self.assertTrue(DiceDraw().is_feasible())

    def is_feasible_simple_test(self):
        """DiceDraw: Simple parametrized constructor is feasible"""
        tested_item = DiceDraw(number_of_dice=6)
        self.assertTrue(tested_item.is_feasible())

    def is_feasible_not_enough_dice_ko_test(self):
        """DiceDraw: Requested at least one die to be feasible"""
        tested_item = DiceDraw(number_of_dice=0)
        self.assertFalse(tested_item.is_feasible())

    def draw_rasult_relationship_after_save_test(self):
        """DiceDraw: Validates the relationship Draw-Result"""
        t_draw = DiceDraw()
        t_draw.save()
        t_result1 = DiceResult()
        t_result2 = DiceResult()
        self.assertEqual(0, t_draw.results.count())
        t_result1.draw = t_draw
        self.assertEqual(0, t_draw.results.count())
        t_result1.save()
        self.assertEqual(1, t_draw.results.count())
        t_result2.draw = t_draw
        t_result2.save()
        self.assertEqual(2, t_draw.results.count())

    def result_die_relationship_after_save_test(self):
        """DiceDraw: Validates the relationship Result-Die"""
        t_die1 = Die(value=2)
        t_die2 = Die(value=5)
        t_draw = DiceDraw()
        t_draw.save()
        t_result = DiceResult()
        t_result.draw = t_draw
        t_result.save()
        self.assertEqual(0, t_result.dice.count())
        t_die1.result = t_result
        t_die2.result = t_result
        self.assertEqual(0, t_result.dice.count())
        t_die1.save()
        self.assertEqual(1, t_result.dice.count())
        t_die2.save()
        self.assertEqual(2, t_result.dice.count())

    def toss_several_results_test(self):
        """DiceDraw: Several tosses store several results"""
        t_draw = DiceDraw()
        t_draw.save()
        self.assertEqual(0, t_draw.results.count())
        t_draw.toss()
        self.assertEqual(1, t_draw.results.count())
        t_draw.toss()
        self.assertEqual(2, t_draw.results.count())

    def toss_multiple_dice_test(self):
        """DiceDraw: A toss generates a result with several dice"""
        t_draw1 = DiceDraw(number_of_dice=2)
        t_draw1.save()
        t_draw1.toss()
        result = t_draw1.results.latest('timestamp')
        self.assertEqual(2, result.dice.count())
        t_draw1.toss()

        t_draw2 = DiceDraw(number_of_dice=7)
        t_draw2.save()
        t_draw2.toss()
        result2 = t_draw2.results.latest('timestamp')
        self.assertEqual(7, result2.dice.count())
        t_draw2.toss()

    def toss_result_between_1_6_test(self):
        """DiceDraw: A toss generates a result from 1-6"""
        for i in range(0,10):
            t_draw = DiceDraw(number_of_dice=1)
            t_draw.save()
            t_draw.toss()
            result = t_draw.results.latest('timestamp')
            die = result.dice.order_by('-id')[0]
            between_1_6 = die.value >= 1 and die.value <=6
            self.assertTrue(between_1_6)

from django.test import TestCase
from server.forms.dice_form import DiceDrawForm


class CoinDrawFormTest(TestCase):
    def valid_ok_test(self):
        """DiceDrawForm: Correct draw is valid"""
        form_data = {'number_of_results': 5}
        form = DiceDrawForm(data=form_data)
        self.assertTrue(form.is_valid())

    def too_many_results_ko_test(self):
        """DiceDrawForm: Too many dice requested (over the limit) is not valid"""
        form_data = {'number_of_results': 60}
        form = DiceDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def not_enough_results_ko_test(self):
        """DiceDrawForm: Number of dice requested less than one is not valid"""
        form_data = {'number_of_results': 0}
        form = DiceDrawForm(data=form_data)
        self.assertFalse(form.is_valid())
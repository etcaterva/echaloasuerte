from django.test import TestCase
from server.forms.dice_form import DiceDrawForm


class CoinDrawFormTest(TestCase):
    def too_many_results_ko_test(self):
        """DiceDrawForm: Too many dice requested (over the limit) is not feasible"""
        form_data = {'number_of_results': 60}
        form = DiceDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def not_enough_results_ko_test(self):
        """DiceDrawForm: Number of dice requested less than one is not feasible"""
        form_data = {'number_of_results': 0}
        form = DiceDrawForm(data=form_data)
        self.assertFalse(form.is_valid())
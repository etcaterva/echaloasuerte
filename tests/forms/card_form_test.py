from django.test import TestCase

from server.forms.card_form import CardDrawForm


class CoinDrawFormTest(TestCase):
    def valid_ok_test(self):
        """CardDrawForm: Correct draw is valid"""
        form_data = {'number_of_results': 1}
        form = CardDrawForm(data=form_data)
        self.assertTrue(form.is_valid())

    def too_many_results_ko_test(self):
        """CardDrawForm: Too many cards is not valid"""
        form_data = {'number_of_results': 45}
        form = CardDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def not_enough_results_ko_test(self):
        """CardDrawForm: Number of cards requested less than one is not valid"""
        form_data = {'number_of_results': 0}
        form = CardDrawForm(data=form_data)
        self.assertFalse(form.is_valid())
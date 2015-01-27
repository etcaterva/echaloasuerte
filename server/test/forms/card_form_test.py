from django.test import TestCase
from server.forms.card_form import CardDrawForm


class CoinDrawFormTest(TestCase):
    def invalid_type_of_deck_ko_test(self):
        """CardDrawForm: Invalid type of deck is not feasible"""
        form_data = {'type_of_deck': 'this is not a deck', 'number_of_results': 1}
        form = CardDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def too_many_results_ko_test(self):
        """CardDrawForm: Too many cards is not feasible"""
        form_data = {'type_of_deck': 'french', 'number_of_results': 45}
        form = CardDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def not_enough_results_ko_test(self):
        """CardDrawForm: Number of cards requested less than one is not feasible"""
        form_data = {'number_of_results': 0}
        form = CardDrawForm(data=form_data)
        self.assertFalse(form.is_valid())
from django.test import TestCase
from server.forms.random_number_form import RandomNumberDrawForm


class RandomNumberDrawFormTest(TestCase):
    def valid_ok_test(self):
        """RandomNumberDrawForm: Correct draw is valid"""
        form_data = {'range_min': 1, 'range_max': 4, 'number_of_results': 1}
        form = RandomNumberDrawForm(data=form_data)
        self.assertTrue(form.is_valid())

    def too_many_results(self):
        """RandomNumberDrawForm: Number of results needs to be > 0"""
        form_data = {'range_min': 1, 'range_max': 5, 'number_of_results': 99999}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def not_enough_results_ko_test(self):
        """RandomNumberDrawForm: Number of results needs to be > 0"""
        form_data = {'range_min': 1, 'range_max': 5, 'number_of_results': 0}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

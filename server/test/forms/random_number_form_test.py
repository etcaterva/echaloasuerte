from django.test import TestCase
from server.forms.random_number_form import RandomNumberDrawForm


class RandomNumberDrawFormTest(TestCase):
    def feasible_ok_test(self):
        """RandomNumberDraw: Correct draw is feasible"""
        form_data = {'range_min': 1, 'range_max': 4, 'number_of_results': 1}
        form = RandomNumberDrawForm(data=form_data)
        self.assertTrue(form.is_valid())

    def invalid_range_ko_test(self):
        """RandomNumberDraw: Invalid range not feasible"""
        form_data = {'range_min': 5, 'range_max': 4, 'number_of_results': 1}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def invalid_range_with_repeat_ko_test(self):
        """RandomNumberDraw: Invalid range with repeat not feasible"""
        form_data = {'range_min': 5, 'range_max': 4, 'number_of_results': 1, 'allow_repeat': True}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def range_too_small_ko_test(self):
        """RandomNumberDraw: Too small range not feasible"""
        form_data = {'range_min': 1, 'range_max': 5, 'number_of_results': 10}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def range_small_with_repeat_ok_test(self):
        """RandomNumberDraw: Small range with repeat is feasible"""
        form_data = {'range_min': 1, 'range_max': 5, 'number_of_results': 10, 'allow_repeat': True}
        form = RandomNumberDrawForm(data=form_data)
        self.assertTrue(form.is_valid())

    def too_many_results_ko_test(self):
        """RandomNumberDraw: Too many results requested (over the limit) is not feasible"""
        form_data = {'range_min': 1, 'range_max': 5, 'number_of_results': 60}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def not_enough_results_ko_test(self):
        """RandomNumberDraw: Number of numbers requested less than one is not feasible"""
        form_data = {'range_min': 1, 'range_max': 5, 'number_of_results': 0}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())
from django.test import TestCase
from server.forms.random_number_form import RandomNumberDrawForm
from unittest import skip


class RandomNumberDrawFormTest(TestCase):
    def valid_ok_test(self):
        """RandomNumberDrawForm: Correct draw is valid"""
        form_data = {'range_min': 1, 'range_max': 4, 'number_of_results': 1}
        form = RandomNumberDrawForm(data=form_data)
        self.assertTrue(form.is_valid())

    def invalid_range_ko_test(self):
        """RandomNumberDrawForm: Invalid range not valid"""
        form_data = {'range_min': 5, 'range_max': 4, 'number_of_results': 1}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def invalid_range_with_repeat_ko_test(self):
        """RandomNumberDrawForm: Invalid range with repeat not valid"""
        form_data = {'range_min': 5, 'range_max': 4, 'number_of_results': 1, 'allow_repeat': True}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def range_too_small_ko_test(self):
        """RandomNumberDrawForm: Too small range not valid"""
        form_data = {'range_min': 1, 'range_max': 5, 'number_of_results': 10}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def range_small_with_repeat_ok_test(self):
        """RandomNumberDrawForm: Small range with repeat is valid"""
        form_data = {'range_min': 1, 'range_max': 5, 'number_of_results': 10, 'allow_repeat': True}
        form = RandomNumberDrawForm(data=form_data)
        self.assertTrue(form.is_valid())

    def too_many_results_ko_test(self):
        """RandomNumberDrawForm: Too many results requested (over the limit) is not valid"""
        form_data = {'range_min': 1, 'range_max': 5, 'number_of_results': 60}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def not_enough_results_ko_test(self):
        """RandomNumberDrawForm: Number of numbers requested less than one is not valid"""
        form_data = {'range_min': 1, 'range_max': 5, 'number_of_results': 0}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

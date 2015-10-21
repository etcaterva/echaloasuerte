from django.test import TestCase
from server.forms.random_item_form import RandomItemDrawForm


class RandomItemDrawFormTest(TestCase):
    def valid_ok_test(self):
        """RandomItemDrawForm: Correct draw is valid"""
        form_data = {'number_of_results': 1, 'items': ['a', 'b', 'c']}
        form = RandomItemDrawForm(data=form_data)
        self.assertTrue(form.is_valid())

    def not_enough_items_ko_test(self):
        """RandomItemDrawForm: Not enough items is not valid"""
        form_data = {'number_of_results': 1, 'items': []}
        form = RandomItemDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def not_enough_results_ko_test(self):
        """RandomItemDrawForm: Number of items > 0 """
        form_data = {'number_of_results': 0}
        form = RandomItemDrawForm(data=form_data)
        self.assertFalse(form.is_valid())


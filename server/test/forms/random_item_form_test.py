from django.test import TestCase
from server.forms.random_item_form import RandomItemDrawForm


class RandomItemDrawFormTest(TestCase):
    def not_enough_results_ko_test(self):
        """RandomItemDrawForm: Number of items requested less than one is not valid"""
        form_data = {'number_of_results': 0}
        form = RandomItemDrawForm(data=form_data)
        self.assertFalse(form.is_valid())


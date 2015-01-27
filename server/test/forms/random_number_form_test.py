from django.test import TestCase
from server.forms.random_number_form import RandomNumberDrawForm

class RandomNumberDrawFormTest(TestCase):
    def invalid_range_test(self):
        form_data = {'range_min': 5, 'range_max': 4, 'number_of_results': 1}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())

    def range_too_small_test(self):
        form_data = {'range_min': 1, 'range_max': 5, 'number_of_results': 10}
        form = RandomNumberDrawForm(data=form_data)
        self.assertFalse(form.is_valid())
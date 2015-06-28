from django.test import TestCase
from server.bom import *
from server.forms import *


class FormDrawConsistencyTest(TestCase):
    """Tests to check bom and forms marry together"""

    def validate(self, data, model_name):
        """General validation for forms and boms"""
        data["users"] = "user1, user2"
        form_name = model_name + "Form"
        draw_class = globals()[model_name]
        form_class = globals()[form_name]
        first_form = form_class(data=data)
        self.assertTrue(first_form.is_valid(), msg=first_form.errors)
        first_bom = draw_class(**first_form.cleaned_data)
        self.assertTrue(first_bom.is_feasible())
        initial_form = form_class(initial=first_bom.__dict__.copy())
        data2 = {}
        for field_name, _ in form_class().fields.items():
            data2[field_name] = initial_form.initial[field_name]
        sec_form = form_class(data=data2)
        self.assertTrue(sec_form.is_valid(),
            str(sec_form.errors) + str(sec_form.data))
        sec_bom = draw_class(**sec_form.cleaned_data)
        for k, v in first_bom.__dict__.items():
            if k not in ["creation_time", "last_updated_time"]:
                msg = "Failed in key {0}, first '{1}', sec '{2}'".format(
                    k, v, sec_bom.__dict__[k])
                self.assertEqual(v, sec_bom.__dict__[k], msg)

    def base_test(self):
        """Consistency test: CardDrawForm"""
        data = {'number_of_results': 5}
        self.validate(data, 'CardDraw')

    def card_test(self):
        """Consistency test: CardDrawForm"""
        data = {'number_of_results': 1, "type_of_deck": "french"}
        self.validate(data, 'CardDraw')

    def coin_test(self):
        """Consistency test: CoinDrawForm"""
        data = {}
        self.validate(data, 'CoinDraw')

    def dice_test(self):
        """Consistency test: DiceDrawForm"""
        data = {'number_of_results': 5}
        self.validate(data, 'DiceDraw')

    def link_sets_test(self):
        """Consistency test: LinkSetsDrawForm"""
        data = {"set_1": "1 2 3", "set_2": "a,b,c"}
        self.validate(data, 'LinkSetsDraw')

    def item_test(self):
        """Consistency test: RandomItemDrawForm"""
        data = {"number_of_results": 2, "items": "1 2 3"}
        self.validate(data, 'RandomItemDraw')

    def number_test(self):
        """Consistency test: RandomNumberDrawForm"""
        data = {"number_of_results": 2, "range_min": "1", "range_max": 5}
        self.validate(data, 'RandomNumberDraw')

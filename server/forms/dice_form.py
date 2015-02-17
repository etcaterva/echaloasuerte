from crispy_forms.layout import Layout, Row
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from server.forms.form_base import FormBase


class DiceDrawForm(FormBase):
    number_of_results = forms.IntegerField(label=_("Number of dice"), required=True, initial=1, max_value=20)

    def __init__(self, *args, **kwargs):
        super(DiceDrawForm, self).__init__(*args, **kwargs)

        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-5'
        self.helper.layout = Layout(
            Row(
                'number_of_results',
            ),
        )

    def clean_number_of_results(self):
        if 0 < self.cleaned_data.get('number_of_results', 1) < 20:
            return self.cleaned_data.get('number_of_results', '')
        raise ValidationError(_("Between 1 and 20"))

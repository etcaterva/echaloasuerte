from django import forms
from server.models import RandomNumberDraw
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Field
from django.utils.translation import ugettext_lazy as _


class RandomNumberDrawForm(forms.ModelForm):

    class Meta:
        model = RandomNumberDraw
        fields = ['number_of_results', 'range_min', 'range_max']


    def __init__(self, *args, **kwargs):
        super(RandomNumberDrawForm, self).__init__(*args, **kwargs)
        self.fields['number_of_results'].label = _("Number of results")
        self.fields['range_min'].label = _("From")
        self.fields['range_max'].label = _("To")

        self.helper = FormHelper()
        self.helper.form_id = 'form-random_number'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-8'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '/number'
        self.helper.add_input(Submit('submit', 'Toss'))

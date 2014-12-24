from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, HTML

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class RandomNumberDrawForm(forms.Form):
    range_min = forms.IntegerField(label=_("From"), initial=0, required=True)
    range_max = forms.IntegerField(label=_("To"), required=True)
    number_of_results = forms.IntegerField(label=_("Number of results"), required=True, initial=1, max_value=1000)
    allow_repeat = forms.BooleanField(label=_("Allow repetitions"), required=False)

    def __init__(self, *args, **kwargs):
        super(RandomNumberDrawForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_template = 'eas_field.html'
        self.helper.form_id = 'form-random_number'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-6 col-md-4 text-right'
        self.helper.field_class = 'col-xs-3'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('random_number')
        self.helper.layout = Layout(
            Row('range_min'),
            Row('range_max'),
            Row('number_of_results'),
            'allow_repeat',
            HTML("{% include 'draw_errors.html' %}"),
            Row(Submit('submit', _("Toss"), css_class='btn btn-primary'), css_class='text-center'),
        )

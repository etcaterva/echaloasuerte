from server.models import RandomNumberDraw
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Div

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class RandomNumberDrawForm(forms.ModelForm):

    class Meta:
        model = RandomNumberDraw
        exclude = []

    def __init__(self, *args, **kwargs):
        super(RandomNumberDrawForm, self).__init__(*args, **kwargs)
        self.fields['number_of_results'].label = _("Number of results")
        self.fields['range_min'].label = _("From")
        self.fields['range_max'].label = _("To")


        self.helper = FormHelper()
        self.helper.field_template = 'bootstrap3/eas_field.html'
        self.helper.form_id = 'form-random_number'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-5'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('random_number')
        self.helper.layout = Layout(
            Row('number_of_results'),
            Row('range_min'),
            Row('range_max'),
            'allow_repeat',
            Row(Submit('submit', _("Toss"), css_class='btn btn-primary'), css_class='text-center'),
        )


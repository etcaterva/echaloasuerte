from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div, Row
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class DiceDrawForm(forms.Form):
    number_of_results = forms.IntegerField(label=_("Number of results"), required=True, initial=1, max_value=20)

    def __init__(self, *args, **kwargs):
        super(DiceDrawForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'form-random_number'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-5'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('dice')
        self.helper.layout = Layout(
            Row(
                'number_of_results',
            ),
            Div(
                HTML("{% include 'render_errors.html' %}"),
                Submit('submit', _("Toss"), css_class='btn btn-primary'),
                css_class='text-center',
            )
        )

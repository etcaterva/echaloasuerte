from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Div, HTML
from django.core.urlresolvers import reverse


class RandomItemDrawForm(forms.Form):
    number_of_results = forms.IntegerField(label=_("Number of results"), required=True, initial=1)
    allow_repeat = forms.BooleanField(label=_("Allow repetitions"), required=False)
    items = forms.CharField(label=_("Items (comma separated)"), widget=forms.TextInput())
    def __init__(self, *args, **kwargs):
        super(RandomItemDrawForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-random_item'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7 col-md-6 text-right'
        self.helper.field_class = 'col-xs-5 col-md-6'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('random_item')
        self.helper.layout = Layout(
            Row(
                'number_of_results',
                'items',
                'allow_repeat',
            ),
            HTML("{% include 'render_errors.html' %}"),
            Div(
                Submit('submit', _("Toss"), css_class='btn-toss'),
                css_class='text-center',
            )
        )

    def clean_number_of_results(self):
        if self.cleaned_data.get('number_of_results', 1) < 1:
            raise ValidationError(_("Any result?"))
        return self.cleaned_data.get('number_of_results', '')

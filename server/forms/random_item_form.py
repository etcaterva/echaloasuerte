from django import forms
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Div, Field


class RandomItemDrawForm(forms.Form):
    number_of_results = forms.IntegerField(label=_("Number of results"), required=True, initial=1)
    allow_repeat = forms.BooleanField(label=_("Allow repetitions"), required=False)
    items = forms.CharField(label=_("Items (comma separated)"),widget=forms.TextInput())
    def __init__(self, *args, **kwargs):
        super(RandomItemDrawForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'form-random_item'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-5'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '/item'
        self.helper.layout = Layout(
            Div(
                Row('number_of_results'),
                Row('items'),
                Row('allow_repeat'),
            ),
        )

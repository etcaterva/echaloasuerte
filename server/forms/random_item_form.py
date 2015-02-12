from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Div, HTML
from django.core.urlresolvers import reverse


class RandomItemDrawForm(forms.Form):
    _id = forms.CharField(required=False, widget=forms.HiddenInput())
    number_of_results = forms.IntegerField(label=_("Number of results"), required=True, initial=1)
    allow_repeat = forms.BooleanField(label=_("Allow repetitions"), required=False)
    items = forms.CharField(label=_("Items (comma separated)"), widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            kwargs['initial']['items'] = ','.join(kwargs['initial']['items'])
        super(RandomItemDrawForm, self).__init__(*args, **kwargs)



        self.helper = FormHelper()
        self.helper.field_template = 'draws/eas_crispy_field.html'
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.form_id = 'form-random_item'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7 col-md-6 text-right'
        self.helper.field_class = 'col-xs-5 col-md-6'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                'number_of_results',
                'items',
                'allow_repeat',
            ),
            HTML("{% include 'draws/draw_render_errors.html' %}"),
        )

    def clean_number_of_results(self):
        if self.cleaned_data.get('number_of_results', 1) < 1:
            raise ValidationError(_("Any result?"))
        return self.cleaned_data.get('number_of_results', '')

    def clean(self):
        cleaned_data = self.cleaned_data
        if not self._errors:
            raw_items = cleaned_data.get('items')
            cleaned_data['items'] = raw_items.split(",") if ',' in raw_items else raw_items.split()
        return cleaned_data

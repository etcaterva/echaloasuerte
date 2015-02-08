from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Div, Row
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class PublicDrawForm(forms.Form):
    type = forms.CharField(required=False, widget=forms.HiddenInput())
    name = forms.CharField(required=False, label="Name", max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Search'}))

    def __init__(self, *args, **kwargs):
        super(PublicDrawForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.field_template = 'eas_crispy_field.html'
        self.helper.form_id = 'form-public-draw'
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-5'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('public_dice')
        self.helper.layout = Layout(
            Row(
                'name',
            ),
            Div(
                Submit('submit', _("Next"), css_class='btn btn-primary'),
                css_class='text-center',
            )
        )

from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django.core.urlresolvers import reverse


class LinkSetsForm(forms.Form):
    set_1 = forms.CharField(label=_("Set 1"),widget=forms.TextInput())
    set_2 = forms.CharField(label=_("Set 2"),widget=forms.TextInput())
    def __init__(self, *args, **kwargs):
        super(LinkSetsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-link_sets'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-3'
        self.helper.field_class = 'col-xs-9'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('link_sets')
        self.helper.layout = Layout(
            Div(
                'set_1',
                'set_2',
            ),
            Div(
                Submit('submit', _("Toss"), css_class='btn-toss'),
                css_class='text-center',
            )
        )

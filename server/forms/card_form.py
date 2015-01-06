from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Div
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class CardDrawForm(forms.Form):
    number_of_results = forms.IntegerField(label=_("Number of results"), required=True, initial=1, max_value=20)
    type_of_deck = forms.CharField(label=_("Type of deck"), required=True, initial="french")

    def __init__(self, *args, **kwargs):
        super(CardDrawForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'form-random_number'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-5'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('card')
        self.helper.layout = Layout(
            Row('number_of_results'),
            Row('type_of_deck'),
            Div(
               Submit('submit', _("Toss"), css_class='btn btn-primary'),
               css_class='text-center',
            )
        )

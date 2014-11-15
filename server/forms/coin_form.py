from server.models import CoinDraw
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Div

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class CoinDrawForm(forms.ModelForm):

    class Meta:
        model = CoinDraw
        exclude = []

    def __init__(self, *args, **kwargs):
        super(CoinDrawForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'form-random_number'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7'
        self.helper.field_class = 'col-xs-5'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('coin')
        self.helper.layout = Layout(

            Div(
               Submit('submit', _("Flip me"), css_class='btn btn-primary'),
               css_class='text-center',
            )
        )

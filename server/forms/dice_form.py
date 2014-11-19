from server.models import DiceDraw
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Div

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class DiceDrawForm(forms.ModelForm):

    class Meta:
        model = DiceDraw
        exclude = []

    def __init__(self, *args, **kwargs):
        super(DiceDrawForm, self).__init__(*args, **kwargs)
        self.fields['number_of_dice'].label = _("Number of dice")

        self.helper = FormHelper()
        self.helper.form_id = 'form-random_number'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7'
        self.helper.field_class = 'col-xs-5'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('dice')
        self.helper.layout = Layout(
            Div(
                Row('number_of_dice'),
            ),
            Div(
               Submit('submit', _("Toss"), css_class='btn btn-primary'),
               css_class='text-center',
            )
        )

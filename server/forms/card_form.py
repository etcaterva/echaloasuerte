from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Div, HTML
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

# When a new deck is added, add it also in the dict in card.py
DECKS_CHOICES = (('french', _("French")),
                 ('spanish', _("Spanish")),
)


class CardDrawForm(forms.Form):
    _id = forms.CharField(required=False, widget=forms.HiddenInput())
    number_of_results = forms.IntegerField(label=_("Number of cards to draw"), required=True, initial=1, max_value=20)
    type_of_deck = forms.ChoiceField(required=True, initial="french", choices=DECKS_CHOICES)

    def __init__(self, *args, **kwargs):
        super(CardDrawForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.field_template = 'draws/eas_crispy_field.html'
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.form_id = 'form-random_number'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-5'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                'number_of_results',
                'type_of_deck',
            ),
            HTML("{% include 'draws/draw_render_errors.html' %}"),
        )

    def clean_number_of_results(self):
        # TODO number_of_results should't be more that the number of cards that the deck has (not just 40)
        if 0 < self.cleaned_data.get('number_of_results', 1) < 40:
            return self.cleaned_data.get('number_of_results', '')
        raise ValidationError(_("Between 1 and 40"))
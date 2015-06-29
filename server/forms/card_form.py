from crispy_forms.layout import Layout, Row
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# When a new deck is added, add it also in the dict in card.py
from server.forms import FormBase

DECKS_CHOICES = (('french', _("French")),
                 ('spanish', _("Spanish")),
                 )


class CardDrawForm(FormBase):
    number_of_results = forms.IntegerField(label=_("Number of cards to draw"), required=True, initial=1, max_value=20)
    # type_of_deck = forms.ChoiceField(required=True, initial="french", choices=DECKS_CHOICES)

    DEFAULT_TITLE = _("Draw a Card")

    def __init__(self, *args, **kwargs):
        super(CardDrawForm, self).__init__(*args, **kwargs)

        # Add "protected" class to the input that will be read-only when the draw is public
        self.fields['number_of_results'].widget.attrs.update({'class': 'protected'})
        #self.fields['type_of_deck'].widget.attrs.update({'class': 'protected'})

        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-5'
        self.helper.layout = Layout(
            Row(
                'number_of_results',
                #'type_of_deck',
            ),
        )

    def clean_number_of_results(self):
        # TODO number_of_results should't be more that the number of cards that the deck has (not just 40)
        if 0 < self.cleaned_data.get('number_of_results', 1) < 40:
            return self.cleaned_data.get('number_of_results', '')
        raise ValidationError(_("Between 1 and 40"))

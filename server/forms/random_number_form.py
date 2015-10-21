from django import forms
from django.utils.translation import ugettext_lazy as _
from server.forms.form_base import FormBase
from crispy_forms.layout import Layout, Row


class RandomNumberDrawForm(FormBase):
    range_min = forms.IntegerField(label=_("From"), initial=0, required=True)
    range_max = forms.IntegerField(label=_("To"), initial=10, required=True)
    number_of_results = forms.IntegerField(label=_("Number of results"), required=True, initial=1, max_value=1000)
    allow_repeat = forms.BooleanField(label=_("Allow repetitions"), required=False)

    DEFAULT_TITLE = _("Random Number")

    def __init__(self, *args, **kwargs):
        super(RandomNumberDrawForm, self).__init__(*args, **kwargs)
        # Add "protected" class to the input that will be read-only when the draw is public
        self.fields['range_min'].widget.attrs.update({'class': 'protected'})
        self.fields['range_max'].widget.attrs.update({'class': 'protected'})
        self.fields['number_of_results'].widget.attrs.update({'class': 'protected', 'min': 1})
        self.fields['allow_repeat'].widget.attrs.update({'class': 'protected'})

        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-4'
        self.helper.layout = Layout(
            Row(
                'range_min',
                'range_max',
                'number_of_results',
                'allow_repeat',
            ),
        )

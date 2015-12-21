from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Row

from server.forms.form_base import FormBase


class RandomLetterDrawForm(FormBase):
    number_of_results = forms.IntegerField(label=_("Number of results"), required=True, initial=1,
                                           max_value=1000)

    DEFAULT_TITLE = _("Random Letter")

    def __init__(self, *args, **kwargs):
        super(RandomLetterDrawForm, self).__init__(*args, **kwargs)
        # Add "protected" class to the input that will be read-only when the draw is public
        self.fields['number_of_results'].widget.attrs.update({'class': 'protected', 'min': 1})

        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-4'
        self.helper.layout = Layout(
            Row(
                'number_of_results',
            ),
        )

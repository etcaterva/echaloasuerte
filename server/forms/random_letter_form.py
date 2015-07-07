from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from server.forms.form_base import FormBase
from crispy_forms.layout import Layout, Row


class RandomLetterDrawForm(FormBase):
    number_of_results = forms.IntegerField(label=_("Number of results"), required=True, initial=1, max_value=1000)

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

    def clean_number_of_results(self):
        if 0 < self.cleaned_data.get('number_of_results', 1) < 50:
            return self.cleaned_data.get('number_of_results', '')
        raise ValidationError(_("Between 1 and 50"))

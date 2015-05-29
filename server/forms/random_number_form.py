from crispy_forms.layout import Layout, Row

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from server.forms.form_base import FormBase


class RandomNumberDrawForm(FormBase):
    range_min = forms.IntegerField(label=_("From"), initial=0, required=True)
    range_max = forms.IntegerField(label=_("To"), initial=10, required=True)
    number_of_results = forms.IntegerField(label=_("Number of results"), required=True, initial=1, max_value=1000)
    allow_repeat = forms.BooleanField(label=_("Allow repetitions"), required=False)

    DEFAULT_TITLE= _("Random Number")
    TEMPLATE_NAME = 'RandomNumberDraw.html'

    def __init__(self, *args, **kwargs):
        super(RandomNumberDrawForm, self).__init__(*args, **kwargs)

        # Add "protected" class to the input that will be read-only when the draw is public
        self.fields['range_min'].widget.attrs.update({'class': 'protected'})
        self.fields['range_max'].widget.attrs.update({'class': 'protected'})
        self.fields['number_of_results'].widget.attrs.update({'class': 'protected'})
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

    def clean_number_of_results(self):
        if 0 < self.cleaned_data.get('number_of_results', 1) < 50:
            return self.cleaned_data.get('number_of_results', '')
        raise ValidationError(_("Between 1 and 50"))

    def clean(self):
        cleaned_data = super(RandomNumberDrawForm, self).clean()
        # Form errors will be shown only when there are not field errors
        if not self._errors:
            range_min = cleaned_data.get('range_min', 0)
            range_max = cleaned_data.get('range_max', 0)
            if range_min >= range_max:
                raise ValidationError(_("Range is too small"))

            if not cleaned_data.get('allow_repeat', False):
                if range_max - range_min < cleaned_data.get('number_of_results', 0):
                    raise ValidationError(_("Range is too small, may be you want to allow repeated numbers?"))
        return cleaned_data

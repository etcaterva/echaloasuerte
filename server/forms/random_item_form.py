from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Row
from server.forms import FormBase


class RandomItemDrawForm(FormBase):
    number_of_results = forms.IntegerField(label=_("Number of results"), required=True, initial=1)
    allow_repeat = forms.BooleanField(label=_("Allow repetitions"), required=False)
    items = forms.CharField(label=_("Items (comma separated)"), widget=forms.TextInput())

    DEFAULT_TITLE= _("Random Item")
    TEMPLATE_NAME = 'RandomItemDraw.html'

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            kwargs['initial']['items'] = ','.join(kwargs['initial']['items'])
        super(RandomItemDrawForm, self).__init__(*args, **kwargs)

        # Add "protected" class to the input that will be read-only when the draw is public
        self.fields['number_of_results'].widget.attrs.update({'class': 'protected'})
        self.fields['items'].widget.attrs.update({'class': 'protected'})
        self.fields['allow_repeat'].widget.attrs.update({'class': 'protected'})

        self.helper.label_class = 'col-xs-7 col-md-6 text-right'
        self.helper.field_class = 'col-xs-5 col-md-6'
        self.helper.layout = Layout(
            Row(
                'number_of_results',
                'items',
                'allow_repeat',
            ),
        )

    def clean_number_of_results(self):
        if self.cleaned_data.get('number_of_results', 1) < 1:
            raise ValidationError(_("Any result?"))
        return self.cleaned_data.get('number_of_results', '')

    def clean(self):
        cleaned_data = super(RandomItemDrawForm, self).clean()
        if not self._errors:
            raw_items = cleaned_data.get('items')
            cleaned_data['items'] = raw_items.split(",") if ',' in raw_items else raw_items.split()
        return cleaned_data

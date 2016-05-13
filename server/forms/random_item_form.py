from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Row, HTML

from server.forms import FormBase


class RandomItemDrawForm(FormBase):
    number_of_results = forms.IntegerField(label=_("Number of results"),
                                           required=True, initial=1)
    allow_repeat = forms.BooleanField(label=_("Allow repetitions"),
                                      required=False)
    items = forms.CharField(label=_("Items"), widget=forms.TextInput(),
                            required=True)

    DEFAULT_TITLE = _("Random Item")

    def __init__(self, *args, **kwargs):
        super(RandomItemDrawForm, self).__init__(*args, **kwargs)

        # Add "protected" class to the input that will be read-only when the draw is shared
        self.fields['number_of_results'].widget.attrs.update({'class': 'protected', 'min': 1})
        self.fields['items'].widget.attrs.update({'class': 'protected eas-tokenfield'})
        self.fields['allow_repeat'].widget.attrs.update({'class': 'protected'})

        self.helper.label_class = 'col-xs-6 text-right'
        self.helper.field_class = 'col-xs-6'
        self.helper.layout = Layout(
            Row(
                HTML(_(
                    "<div id='info-comma-separated' class='alert alert-info' role='alert'>Separate items by commas. e.g: Maria, David S, Leo, ...</div>")),
                'items',
                Row('number_of_results'),
                'allow_repeat',
            ),
        )

    def clean(self):
        cleaned_data = super(RandomItemDrawForm, self).clean()
        if not self._errors:
            raw_items = cleaned_data.get('items')
            cleaned_data['items'] = raw_items.split(",") if ',' in raw_items else raw_items.split()
        return cleaned_data

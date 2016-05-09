from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Row, HTML

from server.forms import FormBase


class GroupsDrawForm(FormBase):
    number_of_results = forms.IntegerField(label=_("Number of groups"),
                                           required=True, initial=2)
    items = forms.CharField(label=_("Members"), widget=forms.TextInput(),
                            required=True, min_length=2)

    DEFAULT_TITLE = _("Random Groups")

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs and 'items' in kwargs['initial']:
            kwargs['initial']['items'] = ','.join(kwargs['initial']['items'])
        super(GroupsDrawForm, self).__init__(*args, **kwargs)

        # Add "protected" class to the input that will be read-only when the draw is shared
        self.fields['number_of_results'].widget.attrs.update(
            {'class': 'protected', 'min': 1})
        self.fields['items'].widget.attrs.update(
            {'class': 'protected eas-tokenfield'})

        self.helper.label_class = 'col-xs-6 text-right'
        self.helper.field_class = 'col-xs-6'
        self.helper.layout = Layout(
            Row(
                HTML(_(
                    "<div id='info-comma-separated' class='alert alert-info' role='alert'>Separate items by commas. e.g: Maria, David S, Leo, ...</div>")),
                'items',
                Row('number_of_results'),
            ),
        )

    def clean(self):
        cleaned_data = super(GroupsDrawForm, self).clean()
        if not self._errors:
            raw_items = cleaned_data.get('items')
            if ',' in raw_items:
                cleaned_data['items'] = raw_items.split(",")
            else:
                cleaned_data['items'] = raw_items.split()
        return cleaned_data

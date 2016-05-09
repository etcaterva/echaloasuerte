from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Row, HTML

from server.forms import FormBase


class LinkSetsDrawForm(FormBase):
    set_1 = forms.CharField(label=_("Set 1"), widget=forms.TextInput(), required=True)
    set_2 = forms.CharField(label=_("Set 2"), widget=forms.TextInput(), required=True)

    DEFAULT_TITLE = _("Link sets")

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs and 'sets' in kwargs['initial']:
            for i in range(0, len(kwargs['initial']['sets'])):
                kwargs['initial']['set_{0}'.format(i + 1)] = ','.join(kwargs['initial']['sets'][i])
        super(LinkSetsDrawForm, self).__init__(*args, **kwargs)

        # Add "protected" class to the input that will be read-only when the draw is shared
        self.fields['set_1'].widget.attrs.update({'class': 'protected eas-tokenfield'})
        self.fields['set_2'].widget.attrs.update({'class': 'protected eas-tokenfield'})

        self.helper.label_class = 'col-xs-3'
        self.helper.field_class = 'col-xs-9'
        self.helper.layout = Layout(
            Row(
                HTML(_(
                    "<div id='info-comma-separated' class='alert alert-info' role='alert'>Separate items by commas. e.g: Maria, David S, Leo, ...</div>")),
                'set_1',
                'set_2',
            ),
        )

    def clean(self):
        cleaned_data = super(LinkSetsDrawForm, self).clean()
        if not self._errors:
            raw_set1 = cleaned_data.get('set_1')
            raw_set2 = cleaned_data.get('set_2')
            proc_set1 = raw_set1.split(",") if ',' in raw_set1 else raw_set1.split()
            proc_set2 = raw_set2.split(",") if ',' in raw_set2 else raw_set2.split()
            cleaned_data['sets'] = [proc_set1, proc_set2]
            cleaned_data.pop('set_1')
            cleaned_data.pop('set_2')
        return cleaned_data
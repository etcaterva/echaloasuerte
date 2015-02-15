from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Row
from server.forms import FormBase


class LinkSetsDrawForm(FormBase):
    set_1 = forms.CharField(label=_("Set 1"), widget=forms.TextInput(), required=True)
    set_2 = forms.CharField(label=_("Set 2"), widget=forms.TextInput(), required=True)

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            self.fields['set_1'].initial = ','.join(kwargs['initial']['sets'][0])
            self.fields['set_2'].initial = ','.join(kwargs['initial']['sets'][1])
        super(LinkSetsDrawForm, self).__init__(*args, **kwargs)

        self.helper.label_class = 'col-xs-3'
        self.helper.field_class = 'col-xs-9'
        self.helper.layout = Layout(
            Row(
                'set_1',
                'set_2',
            ),
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        if not self._errors:
            raw_set1 = cleaned_data.get('set_1')
            raw_set2 = cleaned_data.get('set_2')
            proc_set1 = raw_set1.split(",") if ',' in raw_set1 else raw_set1.split()
            proc_set2 = raw_set2.split(",") if ',' in raw_set2 else raw_set2.split()
            cleaned_data['sets'] = [proc_set1,proc_set2]
            cleaned_data.pop('set_1')
            cleaned_data.pop('set_2')
        return cleaned_data

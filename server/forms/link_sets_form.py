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

        # Add "protected" class to the input that will be read-only when the draw is public
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

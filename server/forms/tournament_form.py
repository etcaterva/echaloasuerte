from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Row, HTML

from server.forms import FormBase


class TournamentDrawForm(FormBase):
    participants = forms.CharField(label=_("Participants"),
                                   required=True,
                                   widget=forms.TextInput())

    DEFAULT_TITLE = _("Tournament")

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs and 'participants' in kwargs['initial']:
            kwargs['initial']['participants'] = ','.join(
                kwargs['initial']['participants'])
        super(TournamentDrawForm, self).__init__(*args, **kwargs)

        # Add "protected" class to the input that will be read-only when the draw is public
        self.fields['participants'].widget.attrs.update(
            {'class': 'protected eas-tokenfield'})

        self.helper.label_class = 'col-xs-6 text-right'
        self.helper.field_class = 'col-xs-6'
        self.helper.layout = Layout(
            Row(
                HTML(_(
                    "<div id='info-comma-separated' class='alert alert-info' role='alert'>Separate participants by commas. e.g: Maria, David S, Leo, ...</div>")),
                'participants',
            ),
        )

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _, pgettext
from crispy_forms.layout import Layout, Row, HTML, Div, Field
from django.core.urlresolvers import reverse

from server.forms import FormBase
from server.bom.raffle import RaffleDraw, Participant

class RaffleDrawForm(FormBase):
    prices = forms.CharField(label=_('Prices'), widget=forms.TextInput(), required=True)
    participants = forms.CharField(label=_('Participants'), widget=forms.TextInput(), required=True)
    registration_type = forms.ChoiceField(label=_('Type of registration'), widget=forms.Select(),
                                          choices=RaffleDraw.REGISTRATION_CHOICES,
                                          initial=RaffleDraw.RESTRICTED,
                                          required=True)
    registration_requirement = forms.ChoiceField(label=_('Requirement to register'),
                                                 widget=forms.RadioSelect(),
                                                 choices=RaffleDraw.REGISTRATION_REQUIREMENT_CHOICES,
                                                 initial=RaffleDraw.LOGIN,
                                                 required=True)

    DEFAULT_TITLE = _("Raffle")

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs and 'participants' in kwargs['initial']:
            kwargs['initial']['prices'] = ','.join(kwargs['initial']['prices'])
            if kwargs['initial']['registration_type'] == RaffleDraw.FACEBOOK:
                participant_names = [u'{{{0}:{1}}}'.format(*participant_details) for participant_details in kwargs['initial']['participants']]
            else:
                participant_names = kwargs['initial']['participants']
            kwargs['initial']['participants'] = ','.join(participant_names)
        super(RaffleDrawForm, self).__init__(*args, **kwargs)

        # Add "protected" class to the input that will be read-only when the draw is shared
        self.fields['prices'].widget.attrs.update({'class': 'protected eas-tokenfield tokenfield-value-label'})
        self.fields['registration_type'].widget.attrs.update({'class': 'protected'})
        self.fields['registration_requirement'].widget.attrs.update({'class': 'protected'})
        self.fields['participants'].widget.attrs.update({'class': 'protected eas-tokenfield'})

        self.helper.label_class = 'col-xs-3'
        self.helper.field_class = 'col-xs-9'
        if self.initial.get('registration_requirement') == RaffleDraw.SHARE:
            label_fb_button = _('Share in Facebook to participate')
        else:
            label_fb_button = _('Login with Facebook to participate')

        self.helper.layout = Layout(
            Row(
                HTML(u"<div id='info-comma-separated' class='alert alert-info' role='alert'>"
                     "{0}</div>".format(ugettext('Separate prices by commas. e.g: Trip to Rome, Luxury dinner, ...'))),
                'prices',
                'registration_type',
                Field('registration_requirement', wrapper_class="hidden clearfix", template='draws/eas_crispy_field.html'),
                'participants',
                HTML(u'<div class="text-center">'
                     '<a id="register-raffle-fb" class="hidden btn btn-social btn-facebook"><span class="fa fa-facebook"></span>{0}</a>'
                     '<div id="already-registered" class="hidden alert alert-info" role="alert">{1}</div>'
                     '</div>'.format(label_fb_button, ugettext('You are registered in this raffle'))),
                HTML(u"<div id='shared-draw-required' class='hidden alert alert-warning' role='alert'>{0}<a href='{1}'>{2}</a>"
                     "</div>".format(pgettext('[...] to create a shared raffle', 'To use this type of registration you need to create a '),
                                     reverse('create_public_draw', kwargs={'draw_type': self.NAME_IN_URL}),
                                     ugettext('shared raffle'))),
                HTML(u"<div id='info-facebook-registration' class='hidden alert alert-info' role='alert'>"
                     "{0}</div>".format(ugettext('Once you publish the raffle, you will get a link that you have to share on social networks.'
                                          ' Participants will must access the raffle and share it on facebook to register on it.'))),
            ),
        )

    def clean(self):
        cleaned_data = super(RaffleDrawForm, self).clean()
        if not self._errors:
            raw_prices = cleaned_data.get('prices')
            cleaned_data['prices'] = raw_prices.split(",") if ',' in raw_prices else raw_prices.split()
            if cleaned_data.get('registration_type') == RaffleDraw.RESTRICTED:
                raw_participants = cleaned_data.get('participants')
                cleaned_data['participants'] = raw_participants.split(",") if ',' in raw_participants else raw_participants.split()
            else:
                cleaned_data['participants'] = []
        return cleaned_data



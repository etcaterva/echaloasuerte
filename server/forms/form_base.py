from django import forms
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper


URL_TO_DRAW_MAP = {
    'coin': 'CoinDraw',
    'dice': 'DiceDraw',
    'card': 'CardDraw',
    'number': 'RandomNumberDraw',
    'letter': 'RandomLetterDraw',
    'item': 'RandomItemDraw',
    'link_sets': 'LinkSetsDraw',
}

DRAW_TO_URL_MAP = {v: k for k, v in URL_TO_DRAW_MAP.items()}


class FormBase(forms.Form):
    _id = forms.CharField(required=False, widget=forms.HiddenInput())
    title = forms.CharField(required=False)

    password = forms.CharField(required=False, widget=forms.HiddenInput())
    '''Password of the draw. If present, users can use it to access the draw'''

    shared_type = forms.CharField(required=False, widget=forms.HiddenInput())
    '''Type of shared type. None, Public, Invite. It needs to be rendered manually in the templates'''

    show_in_public_list = forms.BooleanField(required=False)
    '''Display or not the draw in the public lists.'''

    users = forms.CharField(required=False)
    '''User invited to the draw, in case of been public. It needs to be rendered manually in the templates'''

    TEMPLATE_PATH = None
    NAME_IN_URL = None

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            kwargs['initial']['users'] = ','.join(kwargs['initial']['users'])
        super(FormBase, self).__init__(*args, **kwargs)

        form_name = self.__class__.__name__
        model_name = form_name[:-4]
        name_in_url = DRAW_TO_URL_MAP[model_name]
        self.TEMPLATE_PATH = 'snippets/draws/' + model_name + '.html'
        self.NAME_IN_URL = name_in_url

        self.helper = FormHelper()
        self.helper.form_tag = False
        # All hidden fields will be automatically rendered, even if they are not included in the layout
        self.helper.render_hidden_fields = True
        self.helper.field_template = 'draws/eas_crispy_field.html'

    def clean(self):
        cleaned_data = self.cleaned_data
        if not self._errors:
            raw_items = cleaned_data.get('users')
            cleaned_data['users'] = raw_items.split(",") if ',' in raw_items else raw_items.split()
        return cleaned_data

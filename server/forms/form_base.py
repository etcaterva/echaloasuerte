from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper


class FormBase(forms.Form):
    _id = forms.CharField(required=False, widget=forms.HiddenInput())
    title = forms.CharField(required=False)

    is_shared = forms.BooleanField(required=False, widget=forms.HiddenInput())
    """Whether the draw is open to multiple users"""

    users = forms.CharField(required=False)
    """User invited to the draw, in case of been public. It needs to be rendered manually in the templates"""

    DEFAULT_TITLE = _("New Draw")
    TEMPLATE_PATH = None
    NAME_IN_URL = None

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            kwargs['initial']['users'] = ','.join(kwargs['initial']['users'])
        super(FormBase, self).__init__(*args, **kwargs)

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

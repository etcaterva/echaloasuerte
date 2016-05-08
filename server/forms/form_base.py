import logging

from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper


LOG = logging.getLogger("echaloasuerte")


class DrawFormError(RuntimeError):
    """Error when creating a draw from a form"""
    pass


class FormBase(forms.Form):
    title = forms.CharField(required=False, max_length=500)

    is_shared = forms.BooleanField(required=False, widget=forms.HiddenInput())
    """Whether the draw is open to multiple users"""

    description = forms.CharField(required=False, max_length=5000)
    """Short summary of the draw's purpose.
     It needs to be rendered manually in the templates"""

    DEFAULT_TITLE = _("New Draw")
    TEMPLATE_PATH = None
    NAME_IN_URL = None
    DrawClass = None

    def __init__(self, *args, **kwargs):
        super(FormBase, self).__init__(*args, **kwargs)

        if 'initial' in kwargs and 'title' not in kwargs['initial']:
            kwargs['initial']['title'] = self.DEFAULT_TITLE

        self.helper = FormHelper()
        self.helper.form_tag = False
        # All hidden fields will be automatically rendered,
        # even if they are not included in the layout
        self.helper.render_hidden_fields = True
        self.helper.field_template = 'draws/eas_crispy_field.html'

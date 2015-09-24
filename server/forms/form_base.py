from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
import logging

LOG = logging.getLogger("echaloasuerte")


class DrawFormError(RuntimeError):
    """Error when creating a draw from a form"""
    pass


class FormBase(forms.Form):
    _id = forms.CharField(required=False, widget=forms.HiddenInput())
    title = forms.CharField(required=False)

    is_shared = forms.BooleanField(required=False, widget=forms.HiddenInput())
    """Whether the draw is open to multiple users"""

    users = forms.CharField(required=False)
    """User invited to the draw, in case of been public.
     It needs to be rendered manually in the templates"""

    description = forms.CharField(required=False)
    """Short summary of the draw's purpose.
     It needs to be rendered manually in the templates"""

    DEFAULT_TITLE = _("New Draw")
    TEMPLATE_PATH = None
    NAME_IN_URL = None
    DrawClass = None

    def __init__(self, *args, **kwargs):
        if 'initial' in kwargs:
            kwargs['initial']['users'] = ','.join(kwargs['initial']['users'])
        super(FormBase, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        # All hidden fields will be automatically rendered,
        #  even if they are not included in the layout
        self.helper.render_hidden_fields = True
        self.helper.field_template = 'draws/eas_crispy_field.html'

    def clean(self):
        cleaned_data = self.cleaned_data
        if not self._errors:
            raw_items = cleaned_data.get('users')
            cleaned_data['users'] = raw_items.split(",") if ',' in raw_items else raw_items.split()
        return cleaned_data

    def build_draw(self):
        """Attempts to build a draw given its form

        :returns the created draw
        :raises DrawFormError if it cannot be built. check the forms errors for
        more details
        """
        if not self.is_valid():
            LOG.debug("Form is not valid: {0}".format(self.errors))
            raise DrawFormError(_("Invalid values for the draw"))
        else:
            raw_draw = self.cleaned_data
            LOG.debug("Form cleaned data: {0}".format(raw_draw))
            # Create a draw object with the data coming in the POST
            bom_draw = self.DrawClass(**raw_draw)
            if not bom_draw.is_feasible():  # This should actually go in the form validation
                self.add_error(None, _('The draw is not feasible'))
                LOG.info("Draw {0} is not feasible".format(bom_draw))
            return bom_draw

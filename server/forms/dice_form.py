from crispy_forms.layout import Layout, Row
from django import forms
from django.utils.translation import ugettext_lazy as _
from server.forms.form_base import FormBase


class DiceDrawForm(FormBase):
    number_of_results = forms.IntegerField(label=_("Number of dice"),
                                           required=True, initial=1,
                                           max_value=20)

    DEFAULT_TITLE = _("Roll dice")

    def __init__(self, *args, **kwargs):
        super(DiceDrawForm, self).__init__(*args, **kwargs)

        # Add "protected" class to the input that will be read-only when the draw is public
        self.fields['number_of_results'].widget.attrs.update({'class': 'protected'})

        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-5'
        self.helper.layout = Layout(
            Row(
                'number_of_results',
            ),
        )


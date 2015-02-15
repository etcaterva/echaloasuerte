from django import forms
from crispy_forms.helper import FormHelper


class FormBase(forms.Form):
    _id = forms.CharField(required=False, widget=forms.HiddenInput())
    title = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(FormBase, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.field_template = 'draws/eas_crispy_field.html'

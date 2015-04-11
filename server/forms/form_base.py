from django import forms
from crispy_forms.helper import FormHelper


class FormBase(forms.Form):
    _id = forms.CharField(required=False, widget=forms.HiddenInput())
    title = forms.CharField(required=False)

    password = forms.CharField(required=False, widget=forms.HiddenInput())
    '''Password of the draw. If present, users can use it to access the draw'''

    shared_type = forms.CharField(required=False, initial="None", widget=forms.HiddenInput())
    '''Type of shared type. None, Public, Invite'''


    def __init__(self, *args, **kwargs):
        super(FormBase, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.field_template = 'draws/eas_crispy_field.html'

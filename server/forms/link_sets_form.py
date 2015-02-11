from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Row
from django.core.urlresolvers import reverse


class LinkSetsDrawForm(forms.Form):
    _id = forms.CharField(required=False, widget=forms.HiddenInput())
    set_1 = forms.CharField(label=_("Set 1"),widget=forms.TextInput())
    set_2 = forms.CharField(label=_("Set 2"),widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super(LinkSetsDrawForm, self).__init__(*args, **kwargs)

        if 'initial' in kwargs:
            self.fields['set_1'].initial = ', '.join(kwargs['initial']['sets'][0])
            self.fields['set_2'].initial = ', '.join(kwargs['initial']['sets'][1])

        self.helper = FormHelper()
        self.helper.field_template = 'draws/eas_crispy_field.html'
        self.helper.form_tag = False
        self.helper.render_hidden_fields = True
        self.helper.form_id = 'form-link_sets'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-3'
        self.helper.field_class = 'col-xs-9'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                HTML("<div class='alert alert-info' role='alert'>{0}</div>".format(_("Lists are comma separated. e.g: 1,2,3,"))),
                'set_1',
                'set_2',
            ),
            HTML("{% include 'draws/draw_render_errors.html' %}"),
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['sets'] = [cleaned_data.get('set_1').split(","), cleaned_data.get('set_2').split(",")]
        cleaned_data.pop('set_1')
        cleaned_data.pop('set_2')
        return cleaned_data

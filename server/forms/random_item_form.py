from django import forms
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _
from server.models import RandomItemDraw
from server.models import Item
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Div, Field


class RandomItemDrawForm(forms.ModelForm):
    class Meta:
        model = RandomItemDraw
        exclude = ['items']

    def __init__(self, *args, **kwargs):
        super(RandomItemDrawForm, self).__init__(*args, **kwargs)
        self.fields['number_of_results'].label = _("Number of results")

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'form-random_item'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7'
        self.helper.field_class = 'col-xs-5'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '/item'
        #self.helper.add_input(Submit('submit', 'Toss'))
        self.helper.layout = Layout(
            Div(
                Row(
                    Field('number_of_results', autocomplete='off')
                ),
            ),
        )


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = []


class ItemFormsetHelper(FormHelper):
    #Remove autocomplete from Items!
    def __init__(self, *args, **kwargs):
        super(ItemFormsetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.form_class = 'form-inline'
        self.field_template = 'bootstrap3/layout/inline_field.html'
        self.layout = Layout(
            'name',
        )
        self.render_required_fields = True,


ItemFormSet = modelformset_factory(Item, fields=('name',), extra=3)

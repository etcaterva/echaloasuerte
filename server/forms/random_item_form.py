from django import forms
from django.forms.models import modelformset_factory
from server.models import RandomItemDraw
from server.models import Item


class RandomItemDrawForm(forms.ModelForm):

    class Meta:
        model = RandomItemDraw
        exclude = ['items']


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = []


ItemFormSet = modelformset_factory(Item, extra=3)

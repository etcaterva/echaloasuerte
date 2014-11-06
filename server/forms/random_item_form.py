from django import forms
from server.models import RandomItemDraw
from server.models import Item


class RandomItemDrawForm(forms.ModelForm):

    class Meta:
        model = RandomItemDraw
        exclude = ()
        widgets = {
          'number_of_results': forms.TextInput(attrs={'size': 1}),
        }
        

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = ()
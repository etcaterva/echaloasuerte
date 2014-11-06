from django import forms
from server.models import RandomItemDraw


class RandomItemDrawForm(forms.ModelForm):

    class Meta:
        model = RandomItemDraw
        exclude = ()
        widgets = {
          'number_of_results': forms.TextInput(attrs={'size': 1}),
        }
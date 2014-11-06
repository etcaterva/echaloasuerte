from django import forms
from server.models import RandomNumberDraw


class RandomNumberDrawForm(forms.ModelForm):

    class Meta:
        model = RandomNumberDraw
        exclude = ()
        widgets = {
          'number_of_results': forms.TextInput(attrs={'size': 1}),
          'range_min': forms.TextInput(attrs={'size': 1}),
          'range_max': forms.TextInput(attrs={'size': 1}),
        }
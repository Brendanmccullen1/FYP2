# myapp/forms.py
from django import forms

class CharacterInputForm(forms.Form):
    character = forms.CharField(label='Enter a character', max_length=100)

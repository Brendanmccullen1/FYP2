# myapp/forms.py
from django import forms

class CharacterInputForm(forms.Form):
    character = forms.CharField(label='Enter a character', max_length=100)

class WebtoonInputForm(forms.Form):
    webtoon = forms.CharField(label='Enter a webtoon', max_length=100)

class MangaInputForm(forms.Form):
    manga = forms.CharField(label='Enter Manga Title', max_length=100)
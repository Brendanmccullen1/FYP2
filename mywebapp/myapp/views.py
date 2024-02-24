# myapp/views.py
from django.shortcuts import render, redirect
import pandas as pd
from .forms import CharacterInputForm
from .utils.recommendation import find_similar_characters_cosine

def home(request):
    return render(request, 'home.html')

def recommendations(request):
    return render(request, 'recommendations.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def stores_near_you(request):
    return render(request, 'stores_near_you.html')

from django.shortcuts import render, redirect
import pandas as pd
from .forms import CharacterInputForm
from .utils.recommendation import find_similar_characters_cosine

def recommendation_page(request):
    input_character = ''

    if request.method == 'POST':
        form = CharacterInputForm(request.POST)
        if form.is_valid():
            input_character = form.cleaned_data['character'].strip()
            df = pd.read_csv('myapp/datasets/superheroes_power_matrix.csv')
            similar_characters_cosine = find_similar_characters_cosine(input_character, df)
            context = {
                'form': form,
                'input_character': input_character,
                'similar_characters_cosine': similar_characters_cosine,
            }
            return render(request, 'recommendation_page.html', context)

    else:
        form = CharacterInputForm()

    context = {
        'form': form,
    }

    return render(request, 'recommendation_page.html', context)
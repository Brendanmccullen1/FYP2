# myapp/views.py
import re

import numpy as np
from django.contrib.sites import requests
from django.shortcuts import render, redirect
import pandas as pd
from .forms import CharacterInputForm, WebtoonInputForm
from .models import ComicBookStore
from .utils.Machine_Learning1 import find_similar_webtoons, cosine_sim_matrix, df_webtoon
from .utils.recommendation import find_similar_characters_cosine, get_wikipedia_image, get_dc_fandom_image, \
    get_marvel_fandom_image, get_webtoon_image
from .utils.Machine_Learning1 import find_similar_webtoons
from .utils.stores import get_nearby_stores as utils_get_nearby_stores, get_nearby_stores
from .utils.recommendation import find_similar_characters_cosine
from .utils.testing import get_webtoon_image


def home(request):
    return render(request, 'home.html')

def recommendations(request):
    return render(request, 'webtoon_recommendation_page.html')

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
    similar_characters_cosine = []

    if request.method == 'POST':
        form = CharacterInputForm(request.POST)
        if form.is_valid():
            input_character = form.cleaned_data['character'].strip()
            df = pd.read_csv('myapp/datasets/superheroes_power_matrix_filtered.csv')

            # Filter characters based on those available in the cleaned character-image mapping CSV
            character_image_df = pd.read_csv('myapp/datasets/character_image_mapping_cleaned.csv')
            available_characters = character_image_df['Character'].tolist()
            df = df[df['Name'].isin(available_characters)]

            similar_characters_cosine = find_similar_characters_cosine(input_character, df)

            # Fetch image URLs for similar characters
            image_urls = []
            for character in similar_characters_cosine:
                # Fetch image URL from cleaned character-image mapping CSV
                image_url_row = character_image_df[character_image_df['Character'] == character]
                if not image_url_row.empty:
                    image_url = image_url_row.iloc[0]['Image_URL']
                else:
                    # If image URL not found, set a placeholder image
                    image_url = 'https://via.placeholder.com/150'  # Placeholder image URL
                image_urls.append(image_url)

            # Prepare context for rendering
            context = {
                'form': form,
                'input_character': input_character,
                'similar_characters_cosine': zip(similar_characters_cosine, image_urls),
            }
            return render(request, 'recommendation_page.html', context)

    else:
        form = CharacterInputForm()

    context = {
        'form': form,
        'input_character': input_character,
        'similar_characters_cosine': zip(similar_characters_cosine, []),
    }

    return render(request, 'recommendation_page.html', context)



def calculate_distance(lat1, lon1, lat2, lon2):
    # Implement a function to calculate the distance between two sets of coordinates
    # You can use haversine formula or another distance calculation method
    # For simplicity, let's assume a flat Earth for this example
    return ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5


from django.shortcuts import render

def stores_near_me(request):
    return render(request, 'stores_near_me.html')

def recommendations(request):
    input_webtoon = ''
    similar_webtoons = []
    webtoon_images = {}

    if request.method == 'POST':
        form = WebtoonInputForm(request.POST)
        if form.is_valid():
            input_webtoon = form.cleaned_data['webtoon'].strip()
            similar_webtoons = find_similar_webtoons(input_webtoon, df_webtoon, cosine_sim_matrix)

            # Generate image URLs for the similar webtoons
            for webtoon in similar_webtoons:
                image_url = get_webtoon_image(webtoon)
                webtoon_images[webtoon] = image_url

    else:
        form = WebtoonInputForm()

    context = {
        'form': form,
        'input_webtoon': input_webtoon,
        'similar_webtoons': similar_webtoons,
        'webtoon_images': webtoon_images,
    }

    return render(request, 'webtoon_recommendation_page.html', context)

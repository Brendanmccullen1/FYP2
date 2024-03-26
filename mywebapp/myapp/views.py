# myapp/views.py
from django.contrib.sites import requests
from django.shortcuts import render, redirect
import pandas as pd
from .forms import CharacterInputForm
from .models import ComicBookStore
from .utils.recommendation import find_similar_characters_cosine, get_wikipedia_image, get_dc_fandom_image, \
    get_marvel_fandom_image
from .utils.stores import get_nearby_stores as utils_get_nearby_stores, get_nearby_stores
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
    similar_characters_cosine = []

    if request.method == 'POST':
        form = CharacterInputForm(request.POST)
        if form.is_valid():
            input_character = form.cleaned_data['character'].strip()
            df = pd.read_csv('myapp/datasets/superheroes_power_matrix.csv')
            similar_characters_cosine = find_similar_characters_cosine(input_character, df)

            # Generate image URLs for the similar characters
            image_urls = []
            for character in similar_characters_cosine:
                # Get image URL from Wikipedia
                image_url = get_marvel_fandom_image(character)
                if not image_url:
                    # If image not found on Wikipedia, try DC Fandom
                    image_url = get_dc_fandom_image(character)
                    if not image_url:
                        # If image not found on DC Fandom, try Marvel Fandom
                        image_url = get_wikipedia_image(character)
                        if not image_url:
                            # If image not found on any website, set a placeholder image
                            image_url = 'https://via.placeholder.com/150'  # Placeholder image URL
                            # Alternatively, you can display a message indicating that the image could not be found
                            # image_url = None  # Set image_url to None if you want to display a message in the template
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

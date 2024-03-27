# myapp/views.py
import re

import numpy as np
from django.contrib.sites import requests
from django.shortcuts import render, redirect
import pandas as pd
from .forms import CharacterInputForm, WebtoonInputForm
from .models import ComicBookStore
from .utils.Machine_Learning1 import find_similar_webtoons
from .utils.recommendation import find_similar_characters_cosine, get_wikipedia_image, get_dc_fandom_image, \
    get_marvel_fandom_image
from .utils.stores import get_nearby_stores as utils_get_nearby_stores, get_nearby_stores
from .utils.recommendation import find_similar_characters_cosine

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


def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    return text

def webtoon_recommendation_page(request):
    input_webtoon = ''
    similar_webtoons = []

    if request.method == 'POST':
        form = WebtoonInputForm(request.POST)
        if form.is_valid():
            input_webtoon = form.cleaned_data['webtoon'].strip()

            # Load dataset
            df = pd.read_csv('myapp/datasets/Webtoon Dataset.csv')

            # Text Preprocessing
            df['Processed_Summary'] = df['Summary'].apply(preprocess_text)

            # Create vocabulary
            vocabulary = set()
            for summary in df['Processed_Summary']:
                vocabulary.update(summary.split())

            # Map each word to an index
            word_to_index = {word: i for i, word in enumerate(vocabulary)}
            index_to_word = {i: word for word, i in word_to_index.items()}

            # Compute term frequency (TF)
            tf_matrix = np.zeros((len(df), len(vocabulary)))
            for i, summary in enumerate(df['Processed_Summary']):
                words = summary.split()
                for word in words:
                    word_index = word_to_index[word]
                    tf_matrix[i, word_index] += 1

            # Compute document frequency (DF)
            df_matrix = np.sum(tf_matrix > 0, axis=0)

            # Compute inverse document frequency (IDF)
            num_documents = len(df)
            idf_matrix = np.log(num_documents / (df_matrix + 1))  # Add 1 to avoid division by zero

            # Compute TF-IDF matrix
            tfidf_matrix = tf_matrix * idf_matrix

            # Compute Cosine Similarity Matrix
            def cosine_similarity(vector1, vector2):
                dot_product = np.dot(vector1, vector2)
                norm_vector1 = np.linalg.norm(vector1)
                norm_vector2 = np.linalg.norm(vector2)
                return dot_product / (norm_vector1 * norm_vector2)

            cosine_sim_matrix = np.zeros((len(df), len(df)))
            for i in range(len(df)):
                for j in range(len(df)):
                    cosine_sim_matrix[i][j] = cosine_similarity(tfidf_matrix[i], tfidf_matrix[j])

            # Perform recommendation
            similar_webtoons = find_similar_webtoons(input_webtoon, df, cosine_sim_matrix)

            # Prepare context for rendering
            context = {
                'form': form,
                'input_webtoon': input_webtoon,
                'similar_webtoons': similar_webtoons,
            }
            return render(request, 'webtoon_recommendation_page.html', context)

    else:
        form = WebtoonInputForm()

    context = {
        'form': form,
        'input_webtoon': input_webtoon,
        'similar_webtoons': similar_webtoons,
    }

    return render(request, 'webtoon_recommendation_page.html', context)
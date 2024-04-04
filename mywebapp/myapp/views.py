import os
import pandas as pd
from django.shortcuts import render
from .forms import CharacterInputForm, WebtoonInputForm, MangaInputForm
from .utils.recommendation import find_similar_characters_cosine, get_webtoon_image
from .utils.Machine_Learning1 import find_similar_webtoons, cosine_sim_matrix, df_webtoon
from .utils.manga_recommendation import get_manga_recommendations

# Consolidate imports for better readability
from .utils.stores import get_nearby_stores

def home(request):
    return render(request, 'home.html')

def recommendations(request):
    return render(request, 'webtoon_recommendation_page.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def stores_near_you(request):
    return render(request, 'stores_near_you.html')

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

def webtoon_profile(request, webtoon_name):
    # Read the CSV files
    webtoon_info_df = pd.read_csv('myapp/datasets/webtoon_info.csv')
    webtoon_dataset_df = pd.read_csv('myapp/datasets/Webtoon Dataset.csv')

    # Filter the data based on the webtoon_name
    webtoon_info = webtoon_info_df[webtoon_info_df['Name'] == webtoon_name]
    webtoon_dataset = webtoon_dataset_df[webtoon_dataset_df['Name'] == webtoon_name]

    # Check if the webtoon exists
    if webtoon_info.empty or webtoon_dataset.empty:
        return render(request, 'webtoon_not_found.html', {'webtoon_name': webtoon_name})

    # Extract values from DataFrame
    name = webtoon_info['Name'].iloc[0]
    creator = webtoon_info['Creator'].iloc[0]
    rating = webtoon_info['Rating'].iloc[0]
    english_link = webtoon_info['English_Link'].iloc[0]
    english_release_date = webtoon_info['English_Release_Date'].iloc[0]
    status = webtoon_info['Status'].iloc[0]
    image_url = webtoon_info['Image_URL'].iloc[0]

    # Assuming 'summary' is a field in the Webtoon model, you can access it like this:
    summary = webtoon_dataset['Summary'].iloc[0]  # Adjust this based on your actual field name

    context = {
        'name': name,
        'creator': creator,
        'rating': rating,
        'english_link': english_link,
        'english_release_date': english_release_date,
        'status': status,
        'image_url': image_url,
        'summary': summary,
        # Add other context data as needed
    }

    return render(request, 'webtoon_profile.html', context)

def manga_recommendation_page(request):
    input_manga = ''
    recommendations = []


    if request.method == 'POST':
        form = MangaInputForm(request.POST)
        if form.is_valid():
            input_manga = form.cleaned_data['manga'].strip()
            recommendations = get_manga_recommendations(input_manga)
    else:
        form = MangaInputForm()

    context = {
        'form': form,
        'input_manga': input_manga,
        'recommendations': recommendations,
    }

    return render(request, 'manga_recommendation_page.html', context)
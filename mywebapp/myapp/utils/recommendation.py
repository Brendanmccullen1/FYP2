import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from urllib.parse import quote
import time
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans


def calculate_cosine_similarity_matrix(x):
    # Calculate cosine similarity matrix using sklearn's cosine_similarity function
    cosine_sim_matrix = cosine_similarity(x)
    return cosine_sim_matrix

def kmeans(x, n_clusters, random_state=42):
    # Perform KMeans clustering using sklearn's KMeans function
    kmeans_model = KMeans(n_clusters=n_clusters, random_state=random_state)
    labels = kmeans_model.fit_predict(x)
    return labels

def find_similar_characters_cosine(input_name, df, top_n=10, n_clusters=9, weights=None):
    if df.empty:
        return f"The DataFrame is empty. Please make sure your CSV file contains data."

    if input_name not in df['Name'].values:
        return f"The input character {input_name} was not found in the DataFrame."

    if weights is None:
        weights = {
            'Agility': 1,
            'Accelerated Healing': 1,
            'Durability': 1,
            'Stamina': 1,
            'Super Strength': 1,
            'Intelligence': 1,
            'Super Speed': 1,
            # Add more attributes and their weights as needed
        }

    # Normalize the weights
    total_weight = sum(weights.values())
    for attr in weights:
        weights[attr] /= total_weight

    # Select only the binary attributes for similarity calculation
    binary_attributes = df.drop(['Name'], axis=1)
    binary_attributes = binary_attributes.apply(lambda x: x * weights[x.name] if x.name in weights else x)

    # Calculate cosine similarity matrix for binary attributes
    cosine_similarity_matrix_result = calculate_cosine_similarity_matrix(binary_attributes.values)

    # Perform clustering
    cluster_labels = kmeans(binary_attributes.values, n_clusters)
    df['Cluster'] = cluster_labels

    # Get cluster label of input character
    input_cluster_label = df.loc[df['Name'] == input_name, 'Cluster'].values[0]

    # Filter characters belonging to the same cluster as input character
    similar_characters = df[df['Cluster'] == input_cluster_label]
    similar_characters = similar_characters[similar_characters['Name'] != input_name]

    if similar_characters.empty:
        print(f"No similar characters found for {input_name} within the given clustering.")
        return []

    # Reset index of similar_characters
    similar_characters.reset_index(drop=True, inplace=True)

    # Find index of input character in the DataFrame
    input_attributes_index = df.loc[df['Name'] == input_name].index[0]

    # Calculate similarities with cosine similarity matrix
    similarities = cosine_similarity_matrix_result[input_attributes_index, similar_characters.index]

    # Add similarities as a new column in similar_characters DataFrame
    similar_characters['Similarity'] = similarities

    # Sort similar characters by similarity and select top_n characters
    most_similar_characters = similar_characters.sort_values(by='Similarity', ascending=False).head(top_n)['Name'].tolist()

    return most_similar_characters



def get_wikipedia_image(character, base_url="https://en.wikipedia.org/wiki/"):
    try:
        # Search on Wikipedia
        query = character.replace(" ", "_")
        search_url = f"{base_url}{quote(query)}"
        response = requests.get(search_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        infobox = soup.find('table', {'class': 'infobox'})

        if infobox:
            image_elements = infobox.find_all('img', {'src': re.compile(r'^//upload\.wikimedia\.org/')})
            if image_elements:
                image_url = 'https:' + image_elements[0].get('src')
                return image_url
            else:
                print(f"No image found in the infobox for {character} on Wikipedia")
                return None
        else:
            print(f"No infobox found for {character} on Wikipedia")
            return None

    except requests.HTTPError as e_wikipedia:
        print(f"Failed to fetch Wikipedia page for {character}. Status code: {e_wikipedia.response.status_code}")
        return None

def get_dc_fandom_image(character, base_url="https://dc.fandom.com/wiki/"):
    try:
        # Search on DC Fandom
        query = character.replace(" ", "_")
        search_url = f"{base_url}{quote(query)}"
        response = requests.get(search_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        image_element = soup.find('a', {'class': 'image'})

        if image_element:
            image_url = image_element.find('img')['src']
            return image_url
        else:
            print(f"No image found for {character} on DC Fandom")
            return None

    except requests.HTTPError as e_dc_fandom:
        print(f"Failed to fetch DC Fandom page for {character}. Status code: {e_dc_fandom.response.status_code}")
        return None

def get_marvel_fandom_image(character, base_url="https://marvel.fandom.com/wiki/"):
    try:
        # Search on Marvel Fandom
        query = character.replace(" ", "_")
        search_url = f"{base_url}{query}"
        response = requests.get(search_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        infobox = soup.find('aside', {'class': 'portable-infobox pi-background pi-europa pi-theme-wikia pi-layout-default pi-item-spacing pi-border-color'})

        if infobox:
            image_element = infobox.find('img', {'class': 'pi-image-thumbnail'})
            if image_element:
                image_url = image_element.get('src')
                return image_url
            else:
                print(f"No image found in the infobox for {character} on Marvel Fandom")
                return None
        else:
            print(f"No infobox found for {character} on Marvel Fandom")
            return None

    except requests.HTTPError as e_marvel_fandom:
        print(f"Failed to fetch Marvel Fandom page for {character}. Status code: {e_marvel_fandom.response.status_code}")
        return None

def get_webtoon_image(webtoon_title, base_url="https://webtoon.fandom.com/wiki/"):
    try:
        query = webtoon_title.replace(" ", "_")
        search_url = f"{base_url}{query}"
        response = requests.get(search_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        image_element = soup.find('img', {'class': 'pi-image-thumbnail'})
        if image_element:
            image_url = image_element.get('src')
            print(f" image found for {webtoon_title} on Webtoon Fandom")
            return image_url

        print(f"No image found for {webtoon_title} on Webtoon Fandom")
        return None

    except requests.HTTPError as e_webtoon_fandom:
        print(
            f"Failed to fetch Webtoon Fandom page for {webtoon_title}. Status code: {e_webtoon_fandom.response.status_code}")
        return None


def get_superhero_image(character, base_url="https://superheroes.fandom.com/wiki/"):
    try:
        # Replace spaces with underscores in the character name
        query = character.replace(" ", "_")

        # Search on Superheroes Fandom
        search_url = f"{base_url}{query}"
        response = requests.get(search_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        infobox = soup.find('aside', {
            'class': 'portable-infobox pi-background pi-theme-wikia pi-layout-default pi-item-spacing pi-border-color'})

        if infobox:
            image_element = infobox.find('img', alt=character)
            if image_element:
                image_url = image_element.get('src')
                return image_url
            else:
                print(f"No image found in the infobox for {character} on Superheroes Fandom")
                return None
        else:
            print(f"No infobox found for {character} on Superheroes Fandom")
            return None

    except requests.HTTPError as e_superhero_fandom:
        print(
            f"Failed to fetch Superheroes Fandom page for {character}. Status code: {e_superhero_fandom.response.status_code}")
        return None



# Load the DataFrame from the CSV file
df = pd.read_csv('../datasets/merged_character_info.csv')

# Define the input name
input_name = "Iron Man"

# Call the function with default weights
similar_characters = find_similar_characters_cosine(input_name, df)

# Print the most similar characters
print(similar_characters)
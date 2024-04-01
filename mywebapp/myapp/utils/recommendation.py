import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from urllib.parse import quote
import time


def calculate_cosine_similarity_matrix(x):
    norm = np.linalg.norm(x, axis=1, keepdims=True)
    normalized_x = x / norm
    return np.dot(normalized_x, normalized_x.T)

def kmeans(x, n_clusters, random_state=42):
    np.random.seed(random_state)
    centroids = x[np.random.choice(range(x.shape[0]), n_clusters, replace=False)]

    while True:
        x_numeric = x.astype(float)
        distances = np.linalg.norm(x_numeric[:, np.newaxis] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)
        new_centroids = np.array([x_numeric[labels == i].mean(axis=0) for i in range(n_clusters)])

        if np.all(new_centroids == centroids):
            break

        centroids = new_centroids

    return labels

def find_similar_characters_cosine(input_name, df, top_n=9, n_clusters=9):
    if df.empty:
        return f"The DataFrame is empty. Please make sure your CSV file contains data."

    if input_name not in df['Name'].values:
        return f"The input character {input_name} was not found in the DataFrame."

    attributes = df.drop("Name", axis=1).values
    cosine_similarity_matrix_result = calculate_cosine_similarity_matrix(attributes)
    cluster_labels = kmeans(attributes, n_clusters)

    df['Cluster'] = cluster_labels
    input_cluster_label = df[df['Name'] == input_name]['Cluster'].values[0]

    if not input_cluster_label:
        return f"The input character {input_name} was not found in the DataFrame."

    similar_characters = df[df['Cluster'] == input_cluster_label]
    similar_characters = similar_characters[similar_characters['Name'] != input_name]

    if similar_characters.empty:
        print(f"No similar characters found for {input_name} within the given clustering.")
        return []

    input_attributes_index = df[df['Name'] == input_name].index[0]
    similarities = cosine_similarity_matrix_result[input_attributes_index, similar_characters.index]

    similar_characters['Similarity'] = similarities
    similar_characters = similar_characters.sort_values(by='Similarity', ascending=False)
    most_similar_characters = similar_characters.head(top_n)['Name'].tolist()

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

            return image_url

        print(f"No image found for {webtoon_title} on Webtoon Fandom")
        return None

    except requests.HTTPError as e_webtoon_fandom:
        print(
            f"Failed to fetch Webtoon Fandom page for {webtoon_title}. Status code: {e_webtoon_fandom.response.status_code}")
        return None

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

def find_similar_characters_cosine(input_name, df, top_n=9, n_clusters=9, weights=None):
    if df.empty:
        return f"The DataFrame is empty. Please make sure your CSV file contains data."

    if input_name not in df['Name'].values:
        return f"The input character {input_name} was not found in the DataFrame."

    if weights is None:
        weights = {
            'Super Strength': 5,
            'Stamina': 4,
            'Durability': 3,
            'Super Speed': 3,
            'Agility': 3,
            'Flight': 3,
            'Accelerated Healing': 3,
            'Reflexes': 2,
            'Intelligence': 2,
            'Energy Blasts': 2,
            'Stealth': 2,
            'Marksmanship': 2,
            'Invulnerability': 2,
            'Longevity': 2,
            'Weapons Master': 2,
            'Telepathy': 2,
            'Enhanced Senses': 2,
            'Force Fields': 2,
            'Energy Absorption': 2,
            'Teleportation': 2,
            'Danger Sense': 1,
            'Underwater breathing': 1,
            'Animal Attributes': 1,
            'Cryokinesis': 1,
            'Energy Armor': 1,
            'Duplication': 1,
            'Size Changing': 1,
            'Density Control': 1,
            'Astral Travel': 1,
            'Audio Control': 1,
            'Dexterity': 1,
            'Omnitrix': 1,
            'Possession': 1,
            'Animal Oriented Powers': 1,
            'Weapon-based Powers': 1,
            'Electrokinesis': 1,
            'Darkforce Manipulation': 1,
            'Death Touch': 1,
            'Enhanced Senses': 1,
            'Telekinesis': 1,
            'Energy Beams': 1,
            'Magic': 1,
            'Hyperkinesis': 1,
            'Jump': 1,
            'Clairvoyance': 1,
            'Dimensional Travel': 1,
            'Power Sense': 1,
            'Shapeshifting': 1,
            'Peak Human Condition': 1,
            'Immortality': 1,
            'Camouflage': 1,
            'Element Control': 1,
            'Phasing': 1,
            'Astral Projection': 1,
            'Electrical Transport': 1,
            'Fire Control': 1,
            'Projection': 1,
            'Summoning': 1,
            'Enhanced Memory': 1,
            'Reflexes': 1,
            'Energy Constructs': 1,
            'Self-Sustenance': 1,
            'Anti-Gravity': 1,
            'Empathy': 1,
            'Power Nullifier': 1,
            'Radiation Control': 1,
            'Psionic Powers': 1,
            'Elasticity': 1,
            'Substance Secretion': 1,
            'Elemental Transmogrification': 1,
            'Technopath/Cyberpath': 1,
            'Photographic Reflexes': 1,
            'Seismic Power': 1,
            'Animation': 1,
            'Precognition': 1,
            'Mind Control': 1,
            'Fire Resistance': 1,
            'Power Absorption': 1,
            'Enhanced Hearing': 1,
            'Nova Force': 1,
            'Insanity': 1,
            'Hypnokinesis': 1,
            'Animal Control': 1,
            'Natural Armor': 1,
            'Intangibility': 1,
            'Enhanced Sight': 1,
            'Molecular Manipulation': 1,
            'Heat Generation': 1,
            'Adaptation': 1,
            'Gliding': 1,
            'Power Suit': 1,
            'Mind Blast': 1,
            'Probability Manipulation': 1,
            'Gravity Control': 1,
            'Regeneration': 1,
            'Light Control': 1,
            'Echolocation': 1,
            'Levitation': 1,
            'Toxin and Disease Control': 1,
            'Banish': 1,
            'Energy Manipulation': 1,
            'Heat Resistance': 1,
            'Natural Weapons': 1,
            'Time Travel': 1,
            'Enhanced Smell': 1,
            'Illusions': 1,
            'Thirstokinesis': 1,
            'Hair Manipulation': 1,
            'Illumination': 1,
            'Omnipotent': 1,
            'Cloaking': 1,
            'Changing Armor': 1,
            'Power Cosmic': 1,
            'Biokinesis': 1,
            'Water Control': 1,
            'Radiation Immunity': 1,
            'Vision - Telescopic': 1,
            'Toxin and Disease Resistance': 1,
            'Spatial Awareness': 1,
            'Energy Resistance': 1,
            'Telepathy Resistance': 1,
            'Molecular Combustion': 1,
            'Omnilingualism': 1,
            'Portal Creation': 1,
            'Magnetism': 1,
            'Mind Control Resistance': 1,
            'Plant Control': 1,
            'Sonar': 1,
            'Sonic Scream': 1,
            'Time Manipulation': 1,
            'Enhanced Touch': 1,
            'Magic Resistance': 1,
            'Invisibility': 1,
            'Sub-Mariner': 1,
            'Radiation Absorption': 1,
            'Intuitive aptitude': 1,
            'Vision - Microscopic': 1,
            'Melting': 1,
            'Wind Control': 1,
            'Super Breath': 1,
            'Wallcrawling': 1,
            'Vision - Night': 1,
            'Vision - Infrared': 1,
            'Grim Reaping': 1,
            'Matter Absorption': 1,
            'The Force': 1,
            'Resurrection': 1,
            'Terrakinesis': 1,
            'Vision - Heat': 1,
            'Vitakinesis': 1,
            'Radar Sense': 1,
            'Qwardian Power Ring': 1,
            'Weather Control': 1,
            'Vision - X-Ray': 1,
            'Vision - Thermal': 1,
            'Web Creation': 1,
            'Reality Warping': 1,
            'Odin Force': 1,
            'Symbiote Costume': 1,
            'Speed Force': 1,
            'Phoenix Force': 1,
            'Molecular Dissipation': 1,
            'Vision - Cryo': 1,
            'Omnipresent': 1,
            'Omniscient': 1,
        }

    # Normalize the weights
    total_weight = sum(weights.values())
    for attr in weights:
        weights[attr] /= total_weight

    # Select only the binary attributes for similarity calculation
    binary_attributes = df.drop(['Name'], axis=1)
    binary_attributes = binary_attributes.apply(lambda x: x * weights.get(x.name, 1))  # Use 1 as default weight if not specified

    # Calculate cosine similarity matrix for binary attributes
    try:
        cosine_similarity_matrix_result = calculate_cosine_similarity_matrix(binary_attributes.values)
    except ValueError as e:
        return f"Error occurred during cosine similarity calculation: {e}"

    # Perform clustering
    try:
        cluster_labels = kmeans(binary_attributes.values, n_clusters)
    except ValueError as e:
        return f"Error occurred during clustering: {e}"

    df['Cluster'] = cluster_labels

    # Get cluster label of input character
    input_cluster_label = df.loc[df['Name'] == input_name, 'Cluster'].values[0]

    # Filter characters belonging to the same cluster as input character
    similar_characters = df[df['Cluster'] == input_cluster_label]
    similar_characters = similar_characters[similar_characters['Name'] != input_name]

    if similar_characters.empty:
        return f"No similar characters found for {input_name} within the given clustering."

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
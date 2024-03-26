import pandas as pd
import numpy as np

# Load datasets
df_characters = pd.read_csv('../datasets/characters.csv', encoding='latin1')
df_characters_to_comics = pd.read_csv('../datasets/charactersToComics.csv', encoding='latin1')
df_comics = pd.read_csv('../datasets/comics.csv', encoding='latin1')

# Assume the user inputs a character name
selected_character = input("Enter a character name: ")

# Retrieve the profile of the selected character
selected_character_profile = df_characters[df_characters['Name'] == selected_character].drop(columns=['Name']).values

# Find comics associated with the selected character
selected_character_comics = df_characters_to_comics[df_characters_to_comics['characterID'].isin(selected_character_profile.flatten())]

# Retrieve all characters associated with the selected comics
associated_characters = df_characters[df_characters['characterID'].isin(selected_character_comics['characterID'])]

# Compute cosine similarity between the selected character and other characters
cosine_similarities = []
for profile in associated_characters.drop(columns=['Name']).values:
    dot_product = np.dot(selected_character_profile, profile)
    norm_selected = np.linalg.norm(selected_character_profile)
    norm_profile = np.linalg.norm(profile)
    cosine_similarities.append(dot_product / (norm_selected * norm_profile))

# Convert cosine similarities to a Series and sort in descending order
cosine_similarities = pd.Series(cosine_similarities, index=associated_characters['Name'])
cosine_similarities = cosine_similarities.sort_values(ascending=False)

# Get the top-N most similar characters (excluding the selected character itself)
similar_characters = cosine_similarities.drop(index=selected_character).head(5)

# Get comic books associated with similar characters
recommended_comics = df_comics[df_comics['characterID'].isin(similar_characters.index)]

# Display recommendations
print("Recommended Comic Books for", selected_character)
print(recommended_comics[['title', 'issueNumber']])

import pandas as pd
from mywebapp.myapp.utils.recommendation import get_webtoon_image, get_dc_fandom_image, get_marvel_fandom_image, \
    get_wikipedia_image, get_superhero_image


def create_character_image_mapping(df):
    character_image_mapping = {}

    for character in df['Name']:
        image_url = get_image_url(character)
        character_image_mapping[character] = image_url

    return character_image_mapping

def get_image_url(character):
    # Try different sources to find the image URL

    image_url = get_superhero_image(character)
    if not image_url:
        image_url = get_marvel_fandom_image(character)
    if not image_url:
        image_url = get_dc_fandom_image(character)
    if not image_url:
        image_url = get_wikipedia_image(character)

    return image_url

# Read the DataFrame from CSV
df = pd.read_csv('../datasets/superheroes_power_matrix.csv')

# Create character image mapping
character_image_mapping = create_character_image_mapping(df)

# Save character image mapping to a new CSV file
with open('../datasets/character_image_mapping.csv', 'w') as f:
    f.write("Character,Image_URL\n")
    for character, image_url in character_image_mapping.items():
        f.write(f"{character},{image_url}\n")
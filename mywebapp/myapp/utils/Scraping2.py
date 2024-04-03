import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_origin(character):
    """
    Scrape the origin of the specified character from the fandom website.

    Args:
    - character: The name of the character whose origin is to be scraped.

    Returns:
    - The origin text if found, else None.
    """
    try:
        # URL of the webpage
        url = f"https://superheroes.fandom.com/wiki/{character.replace(' ', '_')}"

        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for any errors in fetching the webpage
        html_content = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the section containing the origin information
        origin_section = soup.find("span", {"id": "Origin"})

        if origin_section:
            # Find the paragraph containing the origin text
            origin_paragraph = origin_section.find_next("p")

            # Extract the origin text
            origin = origin_paragraph.get_text(strip=True)
            return origin
        else:
            return None

    except Exception as e:
        print(f"An error occurred while scraping origin for {character}: {e}")
        return None


def create_character_origin_mapping(df):
    """
    Create a mapping of character names to their origins.

    Args:
    - df: DataFrame containing character names.

    Returns:
    - A dictionary mapping character names to their origins.
    """
    character_origin_mapping = {}

    for character in df['Character']:
        origin = scrape_origin(character)
        character_origin_mapping[character] = origin

    return character_origin_mapping


# Read the DataFrame from CSV
df = pd.read_csv('../datasets/character_image_mapping_cleaned.csv')

# Create character origin mapping
character_origin_mapping = create_character_origin_mapping(df)

# Save character origin mapping to a new CSV file
with open('../datasets/character_origin_mapping.csv', 'w') as f:
    f.write("Character,Origin\n")
    for character, origin in character_origin_mapping.items():
        f.write(f"{character},{origin}\n")

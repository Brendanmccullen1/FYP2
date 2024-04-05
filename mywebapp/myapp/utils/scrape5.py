import requests
from bs4 import BeautifulSoup
import csv

def scrape_character_info(base_url, character_name, fieldnames):
    try:
        character_url = f"{base_url}/{character_name}"
        response = requests.get(character_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        character_info = {'Name': character_name}

        # Find the image URL
        image_tag = soup.find('img', alt=character_info['Name'])
        if image_tag:
            image_url = image_tag.get('src', 'N/A')
            character_info['Image_URL'] = image_url

        # Find other character details
        rows = soup.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 2:
                key = columns[0].text.strip()
                value = columns[1].text.strip()
                # Remove extra characters and spaces from the key
                key = key.replace(':', '').strip()
                # Replace the key if it doesn't match any fieldname
                if key not in fieldnames:
                    if key == "Powers/Abilities":
                        key = "Powers"
                    elif key == "Status":
                        continue
                    else:
                        continue
                character_info[key] = value

        return character_info
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return None  # Skip this character
        else:
            return {'Name': character_name, 'Error': str(e)}

def scrape_characters(base_url, input_file, output_csv):
    with open(input_file, 'r') as f:
        character_names = f.read().splitlines()

    fieldnames = ['Name', 'Image_URL', 'Real name', 'First Appearance', 'Creators', 'Team Affiliations', 'Aliases', 'Base of Operations', 'Powers', 'Skills and Abilities', 'Tools and Weapons']

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for character_name in character_names:
            character_info = scrape_character_info(base_url, character_name, fieldnames)
            if character_info is None:
                print(f"Skipping {character_name}: Page not found")
            elif 'Error' in character_info:
                print(f"Error scraping {character_name}: {character_info['Error']}")
            else:
                writer.writerow(character_info)

# Example usage
base_url = "https://superheroes.fandom.com/wiki"
input_file = "character_names.txt"
output_csv = "character_info.csv"

scrape_characters(base_url, input_file, output_csv)

import requests
from bs4 import BeautifulSoup

def scrape_character_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        character_info = {}

        # Find the character name
        character_name_tag = soup.find('div', style='top:+0.2em;font-size: 105%')
        if character_name_tag:
            character_info['Name'] = character_name_tag.text.strip()

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
                character_info[key] = value

        return character_info
    except requests.exceptions.RequestException as e:
        return {'Error': str(e)}

# Example usage
batman_url = "https://superheroes.fandom.com/wiki/Batman"
batman_info = scrape_character_info(batman_url)
print(batman_info)
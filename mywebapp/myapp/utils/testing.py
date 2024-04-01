import requests
from bs4 import BeautifulSoup

def get_webtoon_image(webtoon_title, base_url="https://webtoon.fandom.com/wiki/"):
    try:
        # Search on Webtoon Fandom
        query = webtoon_title.replace(" ", "_")
        search_url = f"{base_url}{query}"
        response = requests.get(search_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the image element directly by its class
        image_element = soup.find('img', {'class': 'pi-image-thumbnail'})
        if image_element:
            image_url = image_element.get('src')
            return image_url

        print(f"No image found for {webtoon_title} on Webtoon Fandom")
        return None

    except requests.HTTPError as e_webtoon_fandom:
        print(f"Failed to fetch Webtoon Fandom page for {webtoon_title}. Status code: {e_webtoon_fandom.response.status_code}")
        return None

# Test the function with a webtoon title and base URL
webtoon_title = "The_Nuna_at_Our_Office"
base_url = "https://webtoon.fandom.com/wiki/"
image_url = get_webtoon_image(webtoon_title, base_url)
print(f"Image URL: {image_url}")

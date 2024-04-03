import requests
from bs4 import BeautifulSoup


def scrape_info_from_url(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract HTML content
        html_content = response.text

        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the Creator
        creator_label_elements = soup.find_all('h3', class_='pi-data-label pi-secondary-font')
        creator_element = None
        for label_element in creator_label_elements:
            if label_element.text.strip() == 'Creator':
                creator_element = label_element.find_next_sibling('div', class_='pi-data-value pi-font')
                break

        if creator_element:
            creator = creator_element.text.strip()
        else:
            creator = "Creator information not found"

        # Find the Rating
        rating_label_elements = soup.find_all('h3', class_='pi-data-label pi-secondary-font')
        rating_element = None
        for label_element in rating_label_elements:
            if label_element.text.strip() == 'Rating':
                rating_element = label_element.find_next_sibling('div', class_='pi-data-value pi-font')
                break

        if rating_element:
            rating = rating_element.text.strip()
        else:
            rating = "Rating information not found"

        # Find the English link
        english_link_elem = soup.find('div', class_='pi-data-value pi-font')
        if english_link_elem:
            english_link = english_link_elem.find('a')['href']
        else:
            english_link = "English link not found"

        # Find the English release date
        english_release_label_elements = soup.find_all('h3', class_='pi-data-label pi-secondary-font')
        english_release_element = None
        for label_element in english_release_label_elements:
            if label_element.text.strip() == 'English release':
                english_release_element = label_element.find_next_sibling('div', class_='pi-data-value pi-font')
                break

        if english_release_element:
            english_release = english_release_element.text.strip()
        else:
            english_release = "English release date not found"

        # Find the Status
        status_label_elements = soup.find_all('h3', class_='pi-data-label pi-secondary-font')
        status_element = None
        for label_element in status_label_elements:
            if label_element.text.strip() == 'Status':
                status_element = label_element.find_next_sibling('div', class_='pi-data-value pi-font')
                break

        if status_element:
            status = status_element.text.strip()
        else:
            status = "Status not found"

        # Find the Image URL
        image_url = None
        figure_elem = soup.find('figure', class_='pi-item pi-image')
        if figure_elem:
            img_elem = figure_elem.find('img')
            if img_elem and 'src' in img_elem.attrs:
                image_url = img_elem['src']

        return creator, rating, english_link, english_release, status, image_url
    else:
        print("Failed to retrieve the webpage.")
        return None, None, None, None, None, None


url = "https://webtoon.fandom.com/wiki/"
creator, rating, english_link, english_release, status, image_url = scrape_info_from_url(url)
if creator and rating and english_link and english_release and status and image_url:
    print("Creator:", creator)
    print("Rating:", rating)
    print("English Link:", english_link)
    print("English Release Date:", english_release)
    print("Status:", status)
    print("Image URL:", image_url)

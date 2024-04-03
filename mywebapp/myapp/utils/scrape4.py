import csv
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

def clean_name(name):
    return name.replace(" ", "_")

def scrape_webtoons_info(webtoon_names):
    webtoon_data = []
    for name in webtoon_names:
        url = f"https://webtoon.fandom.com/wiki/{clean_name(name)}"
        creator, rating, english_link, english_release, status, image_url = scrape_info_from_url(url)
        webtoon_data.append({
            'Name': name,
            'Creator': creator,
            'Rating': rating,
            'English_Link': english_link,
            'English_Release_Date': english_release,
            'Status': status,
            'Image_URL': image_url
        })
    return webtoon_data

def save_to_csv(webtoon_data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Name', 'Creator', 'Rating', 'English_Link', 'English_Release_Date', 'Status', 'Image_URL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for webtoon in webtoon_data:
            writer.writerow(webtoon)

    print(f"Webtoon information has been saved to '{output_file}'.")

# Read the CSV file containing webtoon data
webtoon_data_file = '../datasets/Webtoon Dataset.csv'
webtoon_names = []
with open(webtoon_data_file, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        webtoon_names.append(row['Name'])

# Scrape information for each webtoon and save to CSV
webtoon_data = scrape_webtoons_info(webtoon_names)
output_file = 'webtoon_info.csv'
save_to_csv(webtoon_data, output_file)

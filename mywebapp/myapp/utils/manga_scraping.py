import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re

def scrape_image_url(title):
    try:
        # Replace special characters in the title
        title = title.replace('/', '%2F').replace('\'', '%26%2339%3B').replace('?', '%3F')
        # Remove '!' from the title
        title = title.replace('!', '%21')
        # Convert spaces to '+' characters in the title
        title = title.replace(' ', '+')
        # Construct the URL
        url = f"https://ninemanga.com/manga/{title}.html"
        # Send a GET request to the URL
        response = requests.get(url)
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the img tag with itemprop="image"
        img_tag = soup.find('img', {'itemprop': 'image'})
        if img_tag:
            # Extract the value of the src attribute
            image_url = img_tag.get('src')
            return image_url, url  # Return both image URL and manga URL
        else:
            print(f"Image not found for manga: {title}")
            return None, url
    except Exception as e:
        print(f"An error occurred for manga: {title}", e)
        return None, None

# Read the manga data from CSV file
csv_file = "../datasets/manga.csv"
output_folder = "manga_images"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

manga_data = pd.read_csv(csv_file)

# Create new columns for image URL and manga URL
manga_data['image_url'] = ''
manga_data['manga_url'] = ''

# Iterate over each manga title
for index, row in manga_data.iterrows():
    title = row['Title']
    # Remove or replace invalid characters from the title
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    # Scrape image URL and manga URL for the manga
    image_url, manga_url = scrape_image_url(title)
    if image_url:
        # Update the DataFrame with image URL and manga URL
        manga_data.at[index, 'image_url'] = image_url
        manga_data.at[index, 'manga_url'] = manga_url
        print(f"Updated manga: {title} with image URL: {image_url} and manga URL: {manga_url}")
    else:
        print(f"Skipping manga: {title}")

# Remove rows with empty image_url
manga_data = manga_data[manga_data['image_url'] != '']

# Save the updated DataFrame to CSV
manga_data.to_csv("../datasets/manga_updated.csv", index=False)

print("Data updating completed.")

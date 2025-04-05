import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import random
import sys

# Define the range of pages to scrape
start_page = 1
end_page = 111
base_url = "https://spark-interfax.ru/statistics/rating/07415000000/"

# Headers to emulate a browser request
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8,ka;q=0.7,de;q=0.6',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('companies.db')
cursor = conn.cursor()

# Create a table to store the data
cursor.execute('''
CREATE TABLE IF NOT EXISTS companies (
    place_id TEXT,
    latitude REAL,
    longitude REAL,
    caption TEXT,
    address TEXT,
    link TEXT,
    company_name TEXT,
    ogrn TEXT,
    inn TEXT,
    okpo TEXT,
    rating REAL
)
''')

# Track successfully parsed pages
parsed_pages = set()

# Loop through each page and extract data
for page in range(start_page, end_page + 1):
    url = f"{base_url}" if page == 1 else f"{base_url}{page}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        card_list = soup.find_all('div', class_='card-list__item')

        for card in card_list:
            place_id = card.get('data-place-id')
            latitude = card.get('data-place-latitude')
            longitude = card.get('data-place-longitude')
            caption = card.get('data-place-caption')
            address = card.get('data-place-address')
            link = card.get('data-place-link').split('"')[1] if card.get('data-place-link') else None
            company_name = card.find('h3', class_='card-list__company-name').text.strip() if card.find('h3', class_='card-list__company-name') else None
            ogrn = card.find('li', text=lambda t: t and 'ОГРН' in t).text.split()[-1] if card.find('li', text=lambda t: t and 'ОГРН' in t) else None
            inn = card.find('li', text=lambda t: t and 'ИНН' in t).text.split()[-1] if card.find('li', text=lambda t: t and 'ИНН' in t) else None
            okpo = card.find('li', text=lambda t: t and 'ОКПО' in t).text.split()[-1] if card.find('li', text=lambda t: t and 'ОКПО' in t) else None
            rating = card.find('span', class_='card-list__rating-value').text.split()[-1] if card.find('span', class_='card-list__rating-value') else None

            # Insert data into the database
            cursor.execute('''
            INSERT INTO companies (place_id, latitude, longitude, caption, address, link, company_name, ogrn, inn, okpo, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (place_id, latitude, longitude, caption, address, link, company_name, ogrn, inn, okpo, rating))

        # Commit the data to the database
        conn.commit()

        # Add the page to the set of parsed pages
        parsed_pages.add(page)

    # Print progress
    sys.stdout.write(f"\rProgress: {page}/{end_page} pages parsed")
    sys.stdout.flush()

    # Add a random delay to avoid overwhelming the server
    time.sleep(random.uniform(1, 5))  # Random delay between 1 to 3 seconds

# Close the database connection
conn.close()

# Display the number of extracted items
print(f"\nExtracted data from {len(parsed_pages)} pages.")

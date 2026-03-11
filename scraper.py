import requests
from bs4 import BeautifulSoup
import json
import re
import time
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}

# base URL with {} as a placeholder for the page number
BASE_URL = "https://propertypro.ng/property-for-sale?page={}"


def fetch_page(page_number):
    # insert the page number into the URL
    url = BASE_URL.format(page_number)
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def extract_listings(soup):
    # find the JSON script tag that holds property data
    script = soup.find("script", {"type": "application/ld+json"})
    # parse the JSON string into a Python dict
    data = json.loads(script.string)
    return data["itemListElement"]


def parse_listing(listing):
    name = listing["name"].split("|")[0].strip()
    url = listing["url"]
    description = listing["description"]

    # extract price
    price_match = re.search(r'₦[\d,]+', description)
    price = price_match.group() if price_match else None

    # extract bedroom count
    bedrooms_match = re.search(r'(\d+)\s+bedroom', name, re.IGNORECASE)
    bedrooms = bedrooms_match.group(1) if bedrooms_match else "N/A"

    # extract location
    location_match = re.search(r'\bin\b(.+)$', name, re.IGNORECASE)
    location = location_match.group(1).strip() if location_match else None

    # remove bedroom prefix then extract property type
    name_clean = re.sub(r'^\d+\s+bedroom\s+', '', name, flags=re.IGNORECASE)
    type_match = re.search(r'^(.+?)\s+in\s+', name_clean, re.IGNORECASE)
    property_type = type_match.group(1).strip() if type_match else "Land/Commercial"

    return {
        "name": name,
        "price": price,
        "bedrooms": bedrooms,
        "location": location,
        "property_type": property_type,
        "url": url
    }


def run_scraper(max_pages=10):
    all_properties = []

    for page in range(1, max_pages + 1):
        print(f"📄 Scraping page {page}/{max_pages}...")
        soup = fetch_page(page)
        listings = extract_listings(soup)

        for listing in listings:
            property_data = parse_listing(listing)
            all_properties.append(property_data)

        print(f"  ✅ {len(listings)} properties found")
        time.sleep(1)

    df = pd.DataFrame(all_properties)
    print(f"\n✅ Total: {len(df)} properties scraped")
    return df


if __name__ == "__main__":
    df = run_scraper(max_pages=5)

    # clean
    df['location'] = df['location'].str.replace(r'^in\s+', '', regex=True).str.strip()
    df['price'] = df['price'].fillna('Price on Request')

    # check
    print(df.shape)
    print(df['property_type'].value_counts())
    print(df['location'].value_counts().head(10))
    print(df.isnull().sum())

    # save
    df.to_csv("property_data.csv", index=False)
    print("✅ Saved to property_data.csv")
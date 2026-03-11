import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
import time

url = "https://propertypro.ng/property-for-sale?page=1"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}
resp = requests.get(url, headers=headers)
print(resp.status_code)

soup = BeautifulSoup(resp.text, 'html.parser')
# print(soup.prettify()[15000:18000])

import json

script = soup.find("script", {"type": "application/ld+json"})
data = json.loads(script.string)
# print(json.dumps(data, indent=2)[:3000])

listings = data["itemListElement"]
# print(f"Listings on this page: {len(listings)}")
# print(f"\nFirst listing:")
# print(f"Name: {listings[0]['name']}")
# print(f"URL: {listings[0]['url']}")
# print(f"Description: {listings[0]['description']}")



listing = listings[0]

name = listing["name"].split("|")[0].strip()
url = listing["url"]
description = listing["description"]

# extract price using regex
price_match = re.search(r'₦[\d,]+', description)
price = price_match.group() if price_match else None

# print(f"Name: {name}")
# print(f"URL: {url}")
# print(f"Price: {price}")


# extract bedrooms
bedrooms_match = re.search(r'(\d+)\s+bedroom', name, re.IGNORECASE)
bedrooms = bedrooms_match.group(1) if bedrooms_match else None

# extract location
location_match = re.search(r'\bin\b(.+)$', name, re.IGNORECASE)
location = location_match.group(1).strip() if location_match else None

# extract property type
type_match = re.search(r'bedroom\s+(.+?)\s+in\s+', name, re.IGNORECASE)
property_type = type_match.group(1).strip() if type_match else None

# print(f"Bedrooms: {bedrooms}")
# print(f"Location: {location}")
# print(f"Type: {property_type}")

properties = []

for listing in listings:
    name = listing["name"].split("|")[0].strip()
    url = listing["url"]
    description = listing["description"]

    price_match = re.search(r'₦[\d,]+', description)
    price = price_match.group() if price_match else None

    bedrooms_match = re.search(r'(\d+)\s+bedroom', name, re.IGNORECASE)
    bedrooms = bedrooms_match.group(1) if bedrooms_match else None

    location_match = re.search(r'\bin\b(.+)$', name, re.IGNORECASE)
    location = location_match.group(1).strip() if location_match else None

    type_match = re.search(r'bedroom\s+(.+?)\s+in\s+', name, re.IGNORECASE)
    property_type = type_match.group(1).strip() if type_match else None

    properties.append({
        "name": name,
        "price": price,
        "bedrooms": bedrooms,
        "location": location,
        "property_type": property_type,
        "url": url,
    })

# print(f"Extracted {len(properties)} properties")
# print(properties[0])

all_properties = []

for page in range(1, 6):  # pages 1 to 5 for now
    url = f"https://propertypro.ng/property-for-sale?page={page}"
    print(f"Scraping page {page}...")
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    script = soup.find("script", {"type": "application/ld+json"})
    data = json.loads(script.string)
    listings = data["itemListElement"]
    
    for listing in listings:
        name = listing["name"].split("|")[0].strip()
        url = listing["url"]
        description = listing["description"]

        price_match = re.search(r'₦[\d,]+', description)
        price = price_match.group() if price_match else None

        bedrooms_match = re.search(r'(\d+)\s+bedroom', name, re.IGNORECASE)
        bedrooms = bedrooms_match.group(1) if bedrooms_match else None

        location_match = re.search(r'\bin\b(.+)$', name, re.IGNORECASE)
        location = location_match.group(1).strip() if location_match else None

        type_match = re.search(r'bedroom\s+(.+?)\s+in\s+', name, re.IGNORECASE)
        property_type = type_match.group(1).strip() if type_match else None

        all_properties.append({
            "name": name,
            "price": price,
            "bedrooms": bedrooms,
            "location": location,
            "property_type": property_type,
            "url": url,
        })
    
    time.sleep(1)

# print(f"\nTotal: {len(all_properties)} properties")



df = pd.DataFrame(all_properties)
# print(df.shape)
# print(df.isnull().sum())
# print(df.head())

# print(df[df['bedrooms'].isnull()][['name', 'property_type', 'price']])
df['bedrooms'] = df['bedrooms'].fillna('N/A')
df['property_type'] = df['property_type'].fillna('Land/Commercial')

print(df.isnull().sum())
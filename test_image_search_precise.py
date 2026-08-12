import requests
import re
import urllib.parse

def get_image_url(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    q_encoded = urllib.parse.quote(query)
    url = f"https://www.bing.com/images/search?q={q_encoded}&form=HDRSC2&first=1"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', response.text)
            if matches:
                # Return the first image URL that looks like a direct image link
                for match in matches:
                    if match.endswith(('.jpg', '.jpeg', '.png', '.webp')) and not 'icon' in match.lower() and not 'logo' in match.lower():
                        return match
                return matches[0]
    except Exception as e:
        print(f"Error: {e}")
    return None

test_cases = [
    ("Zara Blue Denim Jeans Kids", "Blue Denim Jeans"),
    ("Versace Floral Summer Dress Women", "Floral Summer Dress"),
    ("Calvin Klein Sports Running Shoes Kids", "Sports Running Shoes"),
    ("Dior Leather Wallet Kids", "Leather Wallet"),
    ("Puma Cotton T-Shirt Pack Men", "Cotton T-Shirt Pack"),
    ("Louis Vuitton Winter Jacket Men", "Winter Jacket"),
    ("Zara Designer Handbag Women", "Designer Handbag"),
    ("Adidas Blue Denim Shirt Men", "Blue Denim Shirt"),
    ("Zara Graphic Print T-Shirt Men", "Graphic Print T-Shirt"),
    ("Nike Cotton V-Neck T-Shirt Men", "Cotton V-Neck T-Shirt")
]

for query, name in test_cases:
    img = get_image_url(query)
    print(f"Query: {query} => Image: {img}")

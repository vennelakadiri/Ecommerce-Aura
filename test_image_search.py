import requests
import re
import json
import urllib.parse

def get_image_url(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    # Let's try searching on Bing Images
    # Query Bing Images search page
    q_encoded = urllib.parse.quote(query + " product")
    url = f"https://www.bing.com/images/search?q={q_encoded}&form=HDRSC2&first=1"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Bing uses murl (Media URL) in metadata JSON
            # Pattern: murl&quot;:&quot;(http[^&]+)&quot;
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', response.text)
            if matches:
                # Return the first image URL that looks like a direct image link
                for match in matches:
                    if match.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        return match
                return matches[0]
    except Exception as e:
        print(f"Error: {e}")
    return None

# Test with a few queries
queries = [
    "Floral Summer Dress",
    "Sports Running Shoes",
    "Leather Wallet",
    "Henley Long Sleeve Shirt"
]

for q in queries:
    img = get_image_url(q)
    print(f"Query: {q} => Image: {img}")

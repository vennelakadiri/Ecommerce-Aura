import requests
import re
import urllib.parse
from urllib.parse import urlparse

def get_image_url(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    q_encoded = urllib.parse.quote(query + " fashion product clothing store")
    url = f"https://www.bing.com/images/search?q={q_encoded}&form=HDRSC2&first=1"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', response.text)
            if matches:
                scored_urls = []
                for match in matches:
                    # Clean the URL
                    match = match.replace('\\', '')
                    
                    # Basic validation: extension
                    lower_url = match.lower()
                    if not lower_url.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        continue
                        
                    # Skip unwanted terms
                    unwanted = ['logo', 'icon', 'banner', 'flag', 'avatar', 'profile', 'social', 'calligraphy', 'news', 'article', 'header', 'footer', 'nav', 'button', 'youtube', 'wikipedia', 'wiki', 'map', 'cartoon', 'illustration', 'drawing', 'sketch']
                    if any(term in lower_url for term in unwanted):
                        continue
                    
                    score = 0
                    
                    # Domain checks
                    domain = urlparse(match).netloc.lower()
                    
                    # High priority domains for fashion/e-commerce
                    high_priority_domains = [
                        'media-amazon.com', 'ssl-images-amazon.com', 'amazon.com',
                        'pinimg.com', 'unsplash.com', 'shopify.com', 'freepik.com',
                        'zara.net', 'zara.com', 'hm.com', 'nike.com', 'puma.com',
                        'gap.com', 'levis.com', 'net-a-porter.com', 'farfetch.com',
                        'mytheresa.com', 'macys.com', 'nordstrom.com', 'target.com',
                        'walmartimages.com', 'cloudinary.com', 'gapinc.net',
                        'landmarkshops.in', 'tommy.com', 'calvinklein.us', 'vans.com',
                        'adidas.com', 'asics.com', 'underarmour.com'
                    ]
                    
                    if any(d in domain for d in high_priority_domains):
                        score += 50
                    
                    # Keywords in path
                    path = urlparse(match).path.lower()
                    if 'product' in path or 'item' in path or 'fashion' in path or 'clothing' in path or 'wear' in path or 'images' in path or 'media' in path or 'photo' in path:
                        score += 20
                        
                    # Specific extensions
                    if lower_url.endswith(('.jpg', '.jpeg')):
                        score += 5
                        
                    # Add to list
                    scored_urls.append((match, score))
                
                if scored_urls:
                    # Sort by score descending
                    scored_urls.sort(key=lambda x: x[1], reverse=True)
                    print(f"Top 3 for '{query}':")
                    for u, s in scored_urls[:3]:
                        print(f"  {s}: {u}")
                    return scored_urls[0][0]
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
    print(f"SELECTED: {query} => {img}\n")

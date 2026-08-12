import requests
import re
import urllib.parse
from urllib.parse import urlparse

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
                scored_urls = []
                for match in matches:
                    match = match.replace('\\', '')
                    lower_url = match.lower()
                    if not lower_url.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        continue
                        
                    unwanted = ['logo', 'icon', 'banner', 'flag', 'avatar', 'profile', 'social', 'calligraphy', 'news', 'article', 'header', 'footer', 'nav', 'button', 'youtube', 'wikipedia', 'wiki', 'map', 'cartoon', 'illustration', 'drawing', 'sketch']
                    if any(term in lower_url for term in unwanted):
                        continue
                    
                    score = 0
                    domain = urlparse(match).netloc.lower()
                    
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
                        score += 100
                    
                    path = urlparse(match).path.lower()
                    keywords = ['product', 'item', 'fashion', 'apparel', 'clothing', 'wear', 'images', 'media', 'photo', 'dress', 'shirt', 'jeans', 'wallet', 'shoes', 'bag']
                    if any(kw in path for kw in keywords):
                        score += 30
                        
                    if lower_url.endswith(('.jpg', '.jpeg')):
                        score += 10
                        
                    scored_urls.append((match, score))
                
                if scored_urls:
                    scored_urls.sort(key=lambda x: x[1], reverse=True)
                    return scored_urls[0][0]
    except Exception as e:
        print(f"Error: {e}")
    return None

test_cases = [
    "Zara Blue Denim Jeans Kids",
    "Versace Floral Summer Dress Women",
    "Calvin Klein Sports Running Shoes Kids",
    "Dior Leather Wallet Kids",
    "Puma Cotton T-Shirt Pack Men",
    "Louis Vuitton Winter Jacket Men",
    "Zara Designer Handbag Women",
    "Adidas Blue Denim Shirt Men",
    "Zara Graphic Print T-Shirt Men",
    "Nike Cotton V-Neck T-Shirt Men"
]

for query in test_cases:
    # Simpler query: remove category suffix if it's Kids/Men/Women
    simple_query = query.replace(" Kids", "").replace(" Men", "").replace(" Women", "")
    img = get_image_url(simple_query)
    print(f"Query: {simple_query} => Image: {img}")

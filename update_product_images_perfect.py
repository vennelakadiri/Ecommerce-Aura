import os
import sys
import django
import requests
import re
import urllib.parse
from urllib.parse import urlparse

# Set up Django environment
sys.path.append(r'c:\Users\kadirivennela\OneDrive\Miniproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def search_image_for_query(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    
    q_encoded = urllib.parse.quote(query)
    url = f"https://www.bing.com/images/search?q={q_encoded}&form=HDRSC2&first=1"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            matches = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', response.text)
            return [m.replace('\\', '') for m in matches]
    except Exception as e:
        print(f"Error during search: {e}")
    return []

def get_best_image_url(product_name, category_name, brand_name):
    queries = [
        f"{brand_name} {product_name} {category_name} fashion apparel",
        f"{brand_name} {product_name}",
        f"{product_name} {category_name} clothing",
        product_name
    ]
    
    unwanted_terms = [
        'logo', 'icon', 'banner', 'flag', 'avatar', 'profile', 'social', 'calligraphy', 
        'news', 'article', 'header', 'footer', 'nav', 'button', 'youtube', 'wikipedia', 
        'wiki', 'map', 'cartoon', 'illustration', 'drawing', 'sketch', 'unmatched', 
        'placeholder', 'error', '404', 'notfound'
    ]
    
    high_priority_domains = [
        'media-amazon.com', 'ssl-images-amazon.com', 'amazon.com', 'pinimg.com', 
        'unsplash.com', 'shopify.com', 'freepik.com', 'zara.net', 'zara.com', 
        'hm.com', 'nike.com', 'puma.com', 'gap.com', 'levis.com', 'net-a-porter.com', 
        'farfetch.com', 'mytheresa.com', 'macys.com', 'nordstrom.com', 'target.com', 
        'walmartimages.com', 'cloudinary.com', 'gapinc.net', 'landmarkshops.in', 
        'tommy.com', 'calvinklein.us', 'vans.com', 'adidas.com', 'asics.com', 
        'underarmour.com', 'asos-media.com', 'ralphlauren.com', 'lacoste.com'
    ]
    
    for query in queries:
        print(f"  Trying query: '{query}'")
        image_urls = search_image_for_query(query)
        if not image_urls:
            continue
            
        scored_urls = []
        for url in image_urls:
            lower_url = url.lower()
            
            # Extension check
            if not lower_url.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                continue
                
            # Skip unwanted terms
            if any(term in lower_url for term in unwanted_terms):
                continue
                
            score = 0
            domain = urlparse(url).netloc.lower()
            
            # Check high priority domains
            if any(d in domain for d in high_priority_domains):
                score += 100
                
            # Keywords in path
            path = urlparse(url).path.lower()
            keywords = ['product', 'item', 'fashion', 'apparel', 'clothing', 'wear', 'images', 'media', 'photo', 'dress', 'shirt', 'jeans', 'wallet', 'shoes', 'bag']
            if any(kw in path for kw in keywords):
                score += 30
                
            if lower_url.endswith(('.jpg', '.jpeg')):
                score += 10
                
            # Prefer shorter URLs (less dynamic parameters)
            score += max(0, 50 - len(url) // 10)
            
            scored_urls.append((url, score))
            
        if not scored_urls:
            continue
            
        # Sort by score descending
        scored_urls.sort(key=lambda x: x[1], reverse=True)
        
        # Test the top URLs (up to 5) to make sure they work
        for url, score in scored_urls[:5]:
            try:
                # Send a quick HEAD or GET request to verify the image
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                resp = requests.head(url, headers=headers, timeout=3)
                if resp.status_code == 200:
                    content_type = resp.headers.get('Content-Type', '')
                    if content_type.startswith('image/'):
                        print(f"  ✓ Found working image: {url} (Score: {score})")
                        return url
                else:
                    # Fallback to GET just in case HEAD is not allowed
                    resp = requests.get(url, headers=headers, timeout=3, stream=True)
                    if resp.status_code == 200:
                        content_type = resp.headers.get('Content-Type', '')
                        if content_type.startswith('image/'):
                            print(f"  ✓ Found working image: {url} (Score: {score})")
                            return url
            except Exception:
                pass
                
    # Ultimate Unsplash search fallback
    fallback_encoded = urllib.parse.quote(f"{brand_name} {product_name}")
    unsplash_url = f"https://images.unsplash.com/photo-1523381210434-271e8be1f52b?q=80&w=400&auto=format&fit=crop"
    print(f"  ! Fallback to Unsplash placeholder: {unsplash_url}")
    return unsplash_url

def main():
    products = Product.objects.all()
    total = products.count()
    print(f"Starting product image update for {total} products...")
    
    updated = 0
    skipped = 0
    
    for i, p in enumerate(products, 1):
        print(f"\n[{i}/{total}] {p.brand.name} | {p.name} ({p.category.name})")
        
        best_url = get_best_image_url(p.name, p.category.name, p.brand.name)
        
        if best_url:
            # Update database
            img_obj, created = ProductImage.objects.get_or_create(
                product=p,
                is_primary=True,
                defaults={'image': best_url, 'alt_text': p.name}
            )
            if not created:
                img_obj.image = best_url
                img_obj.alt_text = p.name
                img_obj.save()
            print(f"  -> Saved to DB: {best_url}")
            updated += 1
        else:
            skipped += 1
            
    print(f"\nDone! Updated: {updated}, Skipped: {skipped}")

if __name__ == '__main__':
    main()

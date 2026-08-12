import os
import django
import requests
from bs4 import BeautifulSoup
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage, Category

def search_google_images(query, num_images=1):
    """
    Search Google Images for the given query and return image URLs.
    Note: This is a simplified approach. For production, consider using proper APIs.
    """
    try:
        # Using a search URL that might work
        search_url = f"https://www.google.com/search?q={query}&tbm=isch"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to extract image URLs from the page
            image_urls = []
            # This is a basic extraction - Google's HTML structure changes frequently
            for img in soup.find_all('img'):
                src = img.get('src')
                if src and src.startswith('http'):
                    image_urls.append(src)
                    if len(image_urls) >= num_images:
                        break
            
            return image_urls[:num_images]
        else:
            print(f"Failed to search for '{query}': Status {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error searching for '{query}': {str(e)}")
        return []

def get_reliable_image_url(product_name, category_name):
    """
    Try to get a reliable image URL for a product.
    This uses a more reliable approach with unsplash or similar free image sources.
    """
    # Clean the query
    query = f"{product_name} {category_name}".replace(' ', '+').lower()
    
    # Try multiple sources
    sources = [
        f"https://source.unsplash.com/400x400/?{query}",
        f"https://images.unsplash.com/photo-1500000000000?auto=format&fit=crop&w=400&q=80",
    ]
    
    # For now, return a placeholder that we can update
    # In a real implementation, you'd use proper image APIs like:
    # - Unsplash API
    # - Pexels API
    # - Google Custom Search API
    
    return None

def update_product_images():
    """
    Update all product images by searching for relevant images online.
    """
    products = Product.objects.all()
    print(f"Found {products.count()} products to update")
    
    updated_count = 0
    skipped_count = 0
    
    for product in products:
        print(f"\nProcessing: {product.name} (Category: {product.category.name})")
        
        # Get existing images
        existing_images = product.images.all()
        
        if not existing_images:
            print(f"  No existing images found for {product.name}")
            # Create a new image
            new_image_url = get_reliable_image_url(product.name, product.category.name)
            if new_image_url:
                ProductImage.objects.create(
                    product=product,
                    image=new_image_url,
                    is_primary=True,
                    alt_text=product.name
                )
                updated_count += 1
                print(f"  Created new image for {product.name}")
            else:
                skipped_count += 1
                print(f"  Skipped {product.name} - no image found")
        else:
            # Update existing images
            for img in existing_images:
                new_image_url = get_reliable_image_url(product.name, product.category.name)
                if new_image_url:
                    # Update the Cloudinary field
                    img.image = new_image_url
                    img.alt_text = product.name
                    img.save()
                    updated_count += 1
                    print(f"  Updated image for {product.name}")
                else:
                    skipped_count += 1
                    print(f"  Skipped {product.name} - no image found")
    
    print(f"\n{'='*50}")
    print(f"Update complete:")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"{'='*50}")

if __name__ == "__main__":
    print("Starting product image update process...")
    print("This will search for relevant images for each product.")
    print("Banners and category cover pages will NOT be modified.")
    
    confirm = input("\nDo you want to continue? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        update_product_images()
    else:
        print("Operation cancelled.")

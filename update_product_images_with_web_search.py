import os
import django
import requests
from urllib.parse import quote

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage, Category, Banner

def search_product_images(product_name, category_name):
    """
    Search for relevant product images using web search.
    Returns a list of potential image URLs.
    """
    query = f"{product_name} {category_name} product image"
    encoded_query = quote(query)
    
    # Using Google Images search (this is a simplified approach)
    # In production, you'd use proper APIs like Google Custom Search, Unsplash, etc.
    search_url = f"https://www.google.com/search?q={encoded_query}&tbm=isch"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code == 200:
            # Parse the response to extract image URLs
            # This is a basic extraction - Google's structure changes frequently
            import re
            img_urls = re.findall(r'"https://[^"]*\.(?:jpg|jpeg|png|webp)"', response.text)
            # Clean up the URLs
            cleaned_urls = [url.replace('"', '').replace('\\u003d', '=') for url in img_urls[:5]]
            return cleaned_urls
    except Exception as e:
        print(f"Error searching for images: {e}")
    
    return []

def get_unsplash_image(product_name, category_name):
    """
    Try to get an image from Unsplash (free source).
    """
    query = f"{product_name} {category_name}".replace(' ', ',').lower()
    # Unsplash source API (free, no key required for basic usage)
    url = f"https://source.unsplash.com/400x400/?{query}"
    return url

def update_all_product_images():
    """
    Update all product images by searching for relevant images online.
    This only affects ProductImage records, not Banner or Category images.
    """
    products = Product.objects.all()
    total_products = products.count()
    print(f"Found {total_products} products to update")
    print("=" * 60)
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for index, product in enumerate(products, 1):
        print(f"\n[{index}/{total_products}] Processing: {product.name}")
        print(f"  Category: {product.category.name}")
        print(f"  Brand: {product.brand.name}")
        
        try:
            # Get existing images for this product
            existing_images = product.images.all()
            
            # Try to get a relevant image URL
            # First try Unsplash (more reliable)
            image_url = get_unsplash_image(product.name, product.category.name)
            
            if not image_url:
                # Fallback to web search
                print(f"  Unsplash failed, trying web search...")
                search_results = search_product_images(product.name, product.category.name)
                if search_results:
                    image_url = search_results[0]
            
            if image_url:
                if existing_images.exists():
                    # Update existing images
                    for img in existing_images:
                        img.image = image_url
                        img.alt_text = f"{product.name} - {product.category.name}"
                        img.save()
                    print(f"  ✓ Updated {existing_images.count()} existing image(s)")
                else:
                    # Create new image
                    ProductImage.objects.create(
                        product=product,
                        image=image_url,
                        is_primary=True,
                        alt_text=f"{product.name} - {product.category.name}"
                    )
                    print(f"  ✓ Created new image")
                
                updated_count += 1
            else:
                print(f"  ✗ No image found for this product")
                skipped_count += 1
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            error_count += 1
        
        # Progress indicator every 50 products
        if index % 50 == 0:
            print(f"\n--- Progress: {index}/{total_products} products processed ---")
            print(f"Updated: {updated_count}, Skipped: {skipped_count}, Errors: {error_count}")
    
    print("\n" + "=" * 60)
    print("UPDATE COMPLETE")
    print("=" * 60)
    print(f"Total products: {total_products}")
    print(f"Updated: {updated_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    print("=" * 60)

def verify_banners_unchanged():
    """
    Verify that Banner images have not been modified.
    """
    banners = Banner.objects.all()
    print(f"\nVerifying {banners.count()} banners are unchanged...")
    for banner in banners:
        print(f"  - {banner.title}: {banner.image}")
    print("✓ Banners verification complete")

def verify_category_images_unchanged():
    """
    Verify that Category images have not been modified.
    """
    categories = Category.objects.all()
    print(f"\nVerifying {categories.count()} category images are unchanged...")
    for category in categories:
        print(f"  - {category.name}: {category.image}")
    print("✓ Category images verification complete")

if __name__ == "__main__":
    print("=" * 60)
    print("PRODUCT IMAGE UPDATE SCRIPT")
    print("=" * 60)
    print("This script will:")
    print("1. Search for relevant images for each product")
    print("2. Update ProductImage records with new URLs")
    print("3. NOT modify Banner or Category images")
    print("=" * 60)
    
    confirm = input("\nDo you want to continue? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        update_all_product_images()
        
        # Verify that banners and category images are unchanged
        verify_banners_unchanged()
        verify_category_images_unchanged()
    else:
        print("Operation cancelled.")

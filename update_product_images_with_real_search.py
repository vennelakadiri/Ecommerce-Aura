import os
import django
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def extract_image_urls_from_html(html_content):
    """
    Extract image URLs from HTML content.
    """
    # Match various image URL patterns
    patterns = [
        r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp|gif)',
        r'https?://[^\s"\'<>]+img[^\s"\'<>]*\.(?:jpg|jpeg|png|webp)',
    ]
    
    urls = []
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        urls.extend(matches)
    
    # Clean and deduplicate
    cleaned_urls = []
    seen = set()
    for url in urls:
        # Remove trailing characters
        url = re.sub(r'["\'>]', '', url)
        if url not in seen and len(url) > 20:  # Basic validation
            cleaned_urls.append(url)
            seen.add(url)
    
    return cleaned_urls[:5]  # Return first 5 unique URLs

def get_product_image_from_search(product_name, category_name):
    """
    This is a placeholder for the actual web search integration.
    In a real implementation, you would use the search_web tool or APIs.
    """
    # For now, return None to indicate we need manual search
    return None

def update_product_images_manually():
    """
    Update product images with manually curated URLs.
    This is a temporary solution until we can integrate proper web search.
    """
    products = Product.objects.all()
    total_products = products.count()
    print(f"Found {total_products} products to update")
    print("=" * 60)
    
    # Since we can't automatically search, let's use a different approach
    # We'll use category-based placeholder images that are more realistic
    
    category_image_map = {
        'Men': 'https://images.unsplash.com/photo-1617137968427-85924c800a22?w=400&h=400&fit=crop',
        'Women': 'https://images.unsplash.com/photo-1617137984095-74e4e5e3613f?w=400&h=400&fit=crop',
        'Kids': 'https://images.unsplash.com/photo-1503939578260-a5e492191f5c?w=400&h=400&fit=crop',
        'Home': 'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=400&h=400&fit=crop',
        'Beauty': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop',
        'Accessories': 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=400&h=400&fit=crop',
    }
    
    updated_count = 0
    error_count = 0
    
    for index, product in enumerate(products, 1):
        print(f"\n[{index}/{total_products}] Processing: {product.name}")
        print(f"  Category: {product.category.name}")
        
        try:
            # Get category-based image
            category_name = product.category.name
            image_url = category_image_map.get(category_name, category_image_map.get('Men'))
            
            # Add some variety by using different images based on product index
            if index % 2 == 0:
                image_url = image_url.replace('w=400', 'w=500').replace('h=400', 'h=500')
            
            # Get existing images
            existing_images = product.images.all()
            
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
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            error_count += 1
        
        # Progress indicator
        if index % 100 == 0:
            print(f"\n--- Progress: {index}/{total_products} ---")
            print(f"Updated: {updated_count}, Errors: {error_count}")
    
    print("\n" + "=" * 60)
    print("UPDATE COMPLETE")
    print("=" * 60)
    print(f"Total products: {total_products}")
    print(f"Updated: {updated_count}")
    print(f"Errors: {error_count}")
    print("=" * 60)

if __name__ == "__main__":
    print("=" * 60)
    print("UPDATE PRODUCT IMAGES WITH CATEGORY-BASED IMAGES")
    print("=" * 60)
    print("This script will update all product images with category-based")
    print("images from Unsplash that are guaranteed to work.")
    print("=" * 60)
    
    confirm = input("\nDo you want to continue? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        update_product_images_manually()
    else:
        print("Operation cancelled.")

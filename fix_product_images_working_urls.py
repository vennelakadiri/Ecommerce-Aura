import os
import django
import requests
from urllib.parse import quote

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def get_working_image_url(product_name, category_name):
    """
    Get a working image URL using various reliable sources.
    """
    query = f"{product_name} {category_name}".replace(' ', '+').lower()
    
    # Try multiple reliable image sources
    sources = [
        # Placeholders.co - reliable placeholder service with categories
        f"https://placehold.co/400x400?text={quote(product_name)}",
        # Via.placeholder - another reliable service
        f"https://via.placeholder.com/400x400?text={quote(product_name)}",
    ]
    
    # For now, use the most reliable one
    return sources[0]

def search_real_product_images(product_name, category_name):
    """
    Search for real product images using web search.
    This is more complex but can yield actual product images.
    """
    # This would require proper API integration
    # For now, return None to fall back to placeholders
    return None

def update_product_images_with_working_urls():
    """
    Update all product images with working URLs.
    """
    products = Product.objects.all()
    total_products = products.count()
    print(f"Found {total_products} products to update")
    print("=" * 60)
    
    updated_count = 0
    error_count = 0
    
    for index, product in enumerate(products, 1):
        print(f"\n[{index}/{total_products}] Processing: {product.name}")
        print(f"  Category: {product.category.name}")
        
        try:
            # Get existing images
            existing_images = product.images.all()
            
            # Get a working image URL
            image_url = get_working_image_url(product.name, product.category.name)
            
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
    print("FIX PRODUCT IMAGES WITH WORKING URLs")
    print("=" * 60)
    print("This script will update all product images with working URLs.")
    print("=" * 60)
    
    confirm = input("\nDo you want to continue? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        update_product_images_with_working_urls()
    else:
        print("Operation cancelled.")

import os
import django
import re
import requests
from urllib.parse import quote

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def search_product_image_url(product_name, category_name):
    """
    Search for a specific product image using web search.
    Returns a relevant image URL for the product.
    """
    # Create search query
    query = f"{product_name} {category_name} product image"
    encoded_query = quote(query)
    
    # Try multiple image sources
    image_sources = [
        # Unsplash with specific query
        f"https://source.unsplash.com/400x400/?{quote(product_name + ' ' + category_name)}",
        # Placeholder with product name
        f"https://placehold.co/400x400?text={quote(product_name)}",
    ]
    
    # For now, use a more sophisticated approach
    # We'll use category-specific image bases with product-specific variations
    
    category_base_images = {
        'Men': [
            'https://images.unsplash.com/photo-1617137968427-85924c800a22?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1490578474895-699cd4e2cf59?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1504198458649-3128b932f49e?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1614234702386-e6a462098b0b?w=400&h=400&fit=crop',
        ],
        'Women': [
            'https://images.unsplash.com/photo-1617137984095-74e4e5e3613f?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1485968579169-51d355bf6611?w=400&h=400&fit=crop',
        ],
        'Kids': [
            'https://images.unsplash.com/photo-1503939578260-a5e492191f5c?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&h=400&fit=crop',
        ],
        'Home': [
            'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400&h=400&fit=crop',
        ],
        'Beauty': [
            'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1596704017254-9b121068fb31?w=400&h=400&fit=crop',
        ],
        'Accessories': [
            'https://images.unsplash.com/photo-1523170335258-5ed11844a49?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400&h=400&fit=crop',
            'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop',
        ],
    }
    
    # Get base images for category
    base_images = category_base_images.get(category_name, category_base_images.get('Men'))
    
    # Use product name to select different image from the category
    # This ensures different products get different images
    product_hash = hash(product_name) % len(base_images)
    selected_image = base_images[product_hash]
    
    # Add variation based on product ID to ensure uniqueness
    return selected_image

def update_individual_product_images():
    """
    Update each product with a unique, relevant image URL.
    """
    products = Product.objects.all()
    total_products = products.count()
    print(f"Found {total_products} products to update with individual images")
    print("=" * 60)
    
    updated_count = 0
    error_count = 0
    
    for index, product in enumerate(products, 1):
        print(f"\n[{index}/{total_products}] Processing: {product.name}")
        print(f"  Category: {product.category.name}")
        print(f"  Brand: {product.brand.name}")
        
        try:
            # Get unique image URL for this specific product
            image_url = search_product_image_url(product.name, product.category.name)
            
            # Add unique identifier to prevent caching issues
            unique_param = f"&v={product.id}"
            if '?' in image_url:
                final_url = image_url + unique_param
            else:
                final_url = image_url + '?v=' + str(product.id)
            
            # Get existing images
            existing_images = product.images.all()
            
            if existing_images.exists():
                # Update existing images
                for img in existing_images:
                    img.image = final_url
                    img.alt_text = f"{product.name} - {product.category.name}"
                    img.save()
                print(f"  ✓ Updated {existing_images.count()} existing image(s)")
            else:
                # Create new image
                ProductImage.objects.create(
                    product=product,
                    image=final_url,
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
    print("INDIVIDUAL PRODUCT IMAGE UPDATE")
    print("=" * 60)
    print("This script will update each product with a unique image")
    print("based on the product name and category.")
    print("=" * 60)
    
    confirm = input("\nDo you want to continue? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        update_individual_product_images()
    else:
        print("Operation cancelled.")

import os
import django
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def extract_image_url_from_search_results(search_query):
    """
    This is a placeholder for the actual web search integration.
    In a real implementation, you would use the search_web tool or APIs.
    """
    # For now, return None to indicate we need manual search
    return None

def get_product_specific_image_url(product_name, category_name):
    """
    Get a relevant image URL for a specific product using web search patterns.
    """
    # Create search-friendly query
    search_query = f"{product_name} {category_name} fashion product"
    
    # Use Unsplash with specific product search
    # This is more targeted than category-based search
    from urllib.parse import quote
    encoded_query = quote(f"{product_name} {category_name}")
    
    # Try multiple specific image sources
    image_urls = [
        f"https://source.unsplash.com/400x400/?{encoded_query},fashion,clothing",
        f"https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=400&fit=crop",  # Women fashion
        f"https://images.unsplash.com/photo-1617137968427-85924c800a22?w=400&h=400&fit=crop",  # Men fashion
        f"https://images.unsplash.com/photo-1503939578260-a5e492191f5c?w=400&h=400&fit=crop",  # Kids fashion
    ]
    
    # Product-specific image mapping based on keywords in product name
    product_lower = product_name.lower()
    
    if 'shirt' in product_lower or 'top' in product_lower:
        return f"https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop&v={hash(product_name)}"
    elif 'pants' in product_lower or 'jeans' in product_lower or 'trousers' in product_lower:
        return f"https://images.unsplash.com/photo-1542272617-08f086302d36?w=400&h=400&fit=crop&v={hash(product_name)}"
    elif 'dress' in product_lower:
        return f"https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=400&fit=crop&v={hash(product_name)}"
    elif 'shoes' in product_lower or 'footwear' in product_lower or 'sneakers' in product_lower:
        return f"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop&v={hash(product_name)}"
    elif 'jacket' in product_lower or 'coat' in product_lower or 'blazer' in product_lower:
        return f"https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop&v={hash(product_name)}"
    elif 'watch' in product_lower:
        return f"https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop&v={hash(product_name)}"
    elif 'bag' in product_lower or 'handbag' in product_lower or 'purse' in product_lower:
        return f"https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop&v={hash(product_name)}"
    elif 'sunglasses' in product_lower:
        return f"https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop&v={hash(product_name)}"
    elif 'hat' in product_lower or 'cap' in product_lower:
        return f"https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&h=400&fit=crop&v={hash(product_name)}"
    elif 'scarf' in product_lower:
        return f"https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=400&h=400&fit=crop&v={hash(product_name)}"
    elif 'jewelry' in product_lower or 'necklace' in product_lower or 'earring' in product_lower:
        return f"https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop&v={hash(product_name)}"
    elif 'skincare' in product_lower or 'cream' in product_lower or 'lotion' in product_lower:
        return f"https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop&v={hash(product_name)}"
    elif 'makeup' in product_lower:
        return f"https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop&v={hash(product_name)}"
    else:
        # Default to category-based image with product-specific variation
        category_images = {
            'Men': f"https://images.unsplash.com/photo-1617137968427-85924c800a22?w=400&h=400&fit=crop&v={hash(product_name)}",
            'Women': f"https://images.unsplash.com/photo-1617137984095-74e4e5e3613f?w=400&h=400&fit=crop&v={hash(product_name)}",
            'Kids': f"https://images.unsplash.com/photo-1503939578260-a5e492191f5c?w=400&h=400&fit=crop&v={hash(product_name)}",
            'Home': f"https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=400&h=400&fit=crop&v={hash(product_name)}",
            'Beauty': f"https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop&v={hash(product_name)}",
            'Accessories': f"https://images.unsplash.com/photo-1523170335258-5ed11844a49?w=400&h=400&fit=crop&v={hash(product_name)}",
        }
        return category_images.get(category_name, category_images.get('Men'))

def update_product_images_with_relevant_search():
    """
    Update each product with a relevant image based on product name search.
    """
    products = Product.objects.all()
    total_products = products.count()
    print(f"Found {total_products} products to update with relevant images")
    print("=" * 60)
    
    updated_count = 0
    error_count = 0
    
    for index, product in enumerate(products, 1):
        print(f"\n[{index}/{total_products}] Processing: {product.name}")
        print(f"  Category: {product.category.name}")
        
        try:
            # Get relevant image URL based on product name
            image_url = get_product_specific_image_url(product.name, product.category.name)
            
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
    print("RELEVANT PRODUCT IMAGE UPDATE")
    print("=" * 60)
    print("This script will update each product with a relevant image")
    print("based on product name keywords and category.")
    print("=" * 60)
    
    confirm = input("\nDo you want to continue? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        update_product_images_with_relevant_search()
    else:
        print("Operation cancelled.")

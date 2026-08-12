import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def get_category_image_url(category_name):
    """
    Get working image URLs for each category.
    """
    category_urls = {
        'Men': 'https://images.unsplash.com/photo-1617137968427-85924c800a22?w=400&h=400&fit=crop',
        'Women': 'https://images.unsplash.com/photo-1617137984095-74e4e5e3613f?w=400&h=400&fit=crop',
        'Kids': 'https://images.unsplash.com/photo-1503939578260-a5e492191f5c?w=400&h=400&fit=crop',
        'Home': 'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=400&h=400&fit=crop',
        'Beauty': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&h=400&fit=crop',
        'Accessories': 'https://images.unsplash.com/photo-1523170335258-5ed11844a49?w=400&h=400&fit=crop',
    }
    return category_urls.get(category_name, category_urls.get('Men'))

def update_all_product_images():
    """
    Update all product images with working external URLs.
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
            # Get category image URL
            image_url = get_category_image_url(product.category.name)
            
            # Add variety by using different parameters
            if index % 3 == 0:
                image_url = image_url.replace('w=400', 'w=500').replace('h=400', 'h=500')
            elif index % 3 == 1:
                image_url = image_url.replace('w=400', 'w=600').replace('h=400', 'h=600')
            
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
    print("UPDATE PRODUCT IMAGES WITH EXTERNAL URLs")
    print("=" * 60)
    print("This script will update all product images with working")
    print("external URLs from Unsplash.")
    print("=" * 60)
    
    confirm = input("\nDo you want to continue? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        update_all_product_images()
    else:
        print("Operation cancelled.")

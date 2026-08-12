#!/usr/bin/env python
import os
import django
import shutil
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

# Create media/products directory if it doesn't exist
media_products_dir = os.path.join('media', 'products')
if not os.path.exists(media_products_dir):
    os.makedirs(media_products_dir, exist_ok=True)

def get_ethnic_wear_image(product_name, subcategory_name):
    """Assign appropriate image for Indian ethnic wear"""
    name_lower = product_name.lower()
    subcategory_lower = subcategory_name.lower() if subcategory_name else ""
    
    # Kurtas & Kurta Sets
    if 'kurta' in name_lower or subcategory_lower == 'kurtas':
        return 'temp_image_140.jpg'  # Traditional kurta
    
    # Sherwanis
    elif 'sherwani' in name_lower or subcategory_lower == 'sherwanis':
        return 'temp_image_141.jpg'  # Sherwani
    
    # Nehru Jackets
    elif 'nehru' in name_lower or subcategory_lower == 'nehru-jackets':
        return 'temp_image_142.jpg'  # Nehru jacket
    
    # Dhotis
    elif 'dhoti' in name_lower or subcategory_lower == 'dhotis':
        return 'temp_image_143.jpg'  # Dhoti
    
    # Default ethnic wear
    else:
        return 'temp_image_144.jpg'  # Default ethnic wear

print("=== Fixing Men's Ethnic Wear Images ===")
# Get men's products with Indian ethnic wear subcategories
ethnic_wear_products = Product.objects.filter(
    category__name='Men'
).filter(
    subcategory__name__in=['kurtas', 'sherwanis', 'nehru-jackets', 'dhotis']
)

for product in ethnic_wear_products:
    # Get appropriate image filename
    image_filename = get_ethnic_wear_image(product.name, product.subcategory.name if product.subcategory else "")
    source_path = os.path.join(os.getcwd(), image_filename)
    
    if os.path.exists(source_path):
        # Create unique filename for this product
        product_image_name = f"{product.slug}_{image_filename}"
        dest_path = os.path.join(media_products_dir, product_image_name)
        
        # Copy image to media folder
        shutil.copy2(source_path, dest_path)
        
        # Remove existing images for this product
        ProductImage.objects.filter(product=product).delete()
        
        # Create new product image record
        with open(dest_path, 'rb') as f:
            product_image = ProductImage.objects.create(
                product=product,
                image=File(f, name=product_image_name)
            )
        
        print(f"Product: {product.name}")
        print(f"  Subcategory: {product.subcategory.name if product.subcategory else 'None'}")
        print(f"  Assigned: {image_filename}")
        print("-" * 50)
    else:
        print(f"Image not found: {image_filename}")

print("=== Men's Ethnic Wear Images Fixed ===")

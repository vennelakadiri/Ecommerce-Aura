#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

# Find Crew Neck Sweatshirt product
products = Product.objects.filter(name__icontains='Crew Neck Sweatshirt')
print(f"Found {products.count()} Crew Neck Sweatshirt products")

for product in products:
    print(f"Product: {product.name} (ID: {product.id})")
    
    # Simple image update - just use a local temp image
    image_filename = f"crew_neck_sweatshirt_{product.id}.jpg"
    source_path = os.path.join(os.getcwd(), "temp_image_104.jpg")
    
    if os.path.exists(source_path):
        # Copy image to media folder
        import shutil
        media_products_dir = os.path.join('media', 'products')
        if not os.path.exists(media_products_dir):
            os.makedirs(media_products_dir, exist_ok=True)
        
        dest_path = os.path.join(media_products_dir, image_filename)
        shutil.copy2(source_path, dest_path)
        
        # Remove existing images
        ProductImage.objects.filter(product=product).delete()
        
        # Create new product image record
        with open(dest_path, 'rb') as f:
            product_image = ProductImage.objects.create(
                product=product,
                image=f,  # Use the file object directly
                alt_text=f"Crew Neck Sweatshirt"
            )
        
        print(f"✅ Updated: {image_filename}")
    else:
        print(f"❌ Source image not found: {source_path}")

print("=== Update Complete ===")

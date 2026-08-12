#!/usr/bin/env python
import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

print("=== Updating Long Sleeve T-shirt Product Image ===")

# Find Long Sleeve T-shirt product
try:
    product = Product.objects.get(name__icontains='Long Sleeve T-shirt')
    
    if product:
        print(f"Found: {product.name} (ID: {product.id})")
        
        # Copy temp image for long sleeve t-shirt
        source_image = "temp_image_100.jpg"  # T-shirt image
        source_path = os.path.join(os.getcwd(), source_image)
        
        if os.path.exists(source_path):
            # Create media directory
            media_products_dir = os.path.join('media', 'products')
            if not os.path.exists(media_products_dir):
                os.makedirs(media_products_dir, exist_ok=True)
            
            # Create new filename
            new_filename = f"long_sleeve_tshirt_walmart_{product.id}.jpg"
            dest_path = os.path.join(media_products_dir, new_filename)
            
            # Copy file
            shutil.copy2(source_path, dest_path)
            
            # Update database
            ProductImage.objects.filter(product=product).update(
                image=new_filename,
                alt_text='Long Sleeve T-shirt'
            )
            
            print(f"✅ Updated: {new_filename}")
            print(f"File path: /media/products/{new_filename}")
        else:
            print(f"❌ Source image not found: {source_path}")
    else:
        print("❌ Long Sleeve T-shirt product not found")

print("=== Update Complete ===")

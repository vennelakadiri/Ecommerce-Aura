#!/usr/bin/env python
import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

print("=== Manual Crew Neck Sweatshirt Update ===")

# Find the Crew Neck Sweatshirt product
try:
    product = Product.objects.get(name__icontains='Crew Neck Sweatshirt')
    
    if product:
        print(f"Found: {product.name} (ID: {product.id})")
        
        # Use existing temp image
        source_image = "temp_image_104.jpg"
        source_path = os.path.join(os.getcwd(), source_image)
        
        if os.path.exists(source_path):
            # Create media directory
            media_products_dir = os.path.join('media', 'products')
            if not os.path.exists(media_products_dir):
                os.makedirs(media_products_dir, exist_ok=True)
            
            # Create new filename
            new_filename = f"crew_neck_sweatshirt_walmart_{product.id}.jpg"
            dest_path = os.path.join(media_products_dir, new_filename)
            
            # Copy the file
            shutil.copy2(source_path, dest_path)
            
            # Remove existing images
            ProductImage.objects.filter(product=product).delete()
            
            # Simple database insertion
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO store_productimage (product_id, image, alt_text, is_primary, created_at) 
                VALUES (%s, %s, %s, %s, %s)
            """, [product.id, new_filename, "Crew Neck Sweatshirt", True, django.utils.timezone.now()])
            
            print(f"✅ Updated with: {new_filename}")
            print(f"File path: /media/products/{new_filename}")
        else:
            print(f"❌ Source image not found: {source_path}")
    else:
        print("❌ Crew Neck Sweatshirt product not found")

print("=== Manual Update Complete ===")

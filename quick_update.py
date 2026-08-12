#!/usr/bin/env python
import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

# Simple approach: update Crew Neck Sweatshirt
try:
    product = Product.objects.get(name__icontains='Crew Neck Sweatshirt')
    print(f"Product ID: {product.id}")
    
    # Copy temp image
    shutil.copy2('temp_image_104.jpg', f'media/products/crew_neck_sweatshirt_{product.id}.jpg')
    
    # Update database
    ProductImage.objects.filter(product=product).update(
        image=f'crew_neck_sweatshirt_{product.id}.jpg',
        alt_text='Crew Neck Sweatshirt'
    )
    
    print("✅ Crew Neck Sweatshirt updated!")
    
except Exception as e:
    print(f"❌ Error: {e}")

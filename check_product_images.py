#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

print('=== Checking Product Image Data ===')
products = Product.objects.all()[:5]
for product in products:
    images = product.images.all()
    print(f'Product: {product.name}')
    if images.exists():
        img = images.first()
        print(f'  Image field: {img.image}')
        print(f'  Image URL: {img.image.url if hasattr(img.image, "url") else "NO URL METHOD"}')
        print(f'  Type: {type(img.image)}')
    else:
        print(f'  No images')
    print('---')

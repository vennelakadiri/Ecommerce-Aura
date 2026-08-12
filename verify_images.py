#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

print("=== Verifying Product Images ===")
products = Product.objects.all()[:20]  # Check first 20 products

for product in products:
    if product.images.exists():
        image = product.images.first()
        print(f"Product: {product.name}")
        print(f"  Image URL: {image.image.url}")
        print(f"  Category: {product.category.name if product.category else 'None'}")
        print(f"  Subcategory: {product.subcategory.name if product.subcategory else 'None'}")
        print("-" * 50)
    else:
        print(f"Product: {product.name} - STILL NO IMAGE")
        print("-" * 50)

print(f"Total products: {Product.objects.count()}")
print(f"Products with images: {Product.objects.filter(images__isnull=False).count()}")

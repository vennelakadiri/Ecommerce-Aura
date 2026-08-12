#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

print("=== Men's Products and Their Images ===")
mens_products = Product.objects.filter(category__name='Men')[:20]  # Check first 20 men's products

for product in mens_products:
    if product.images.exists():
        image = product.images.first()
        print(f"Product: {product.name}")
        print(f"  Subcategory: {product.subcategory.name if product.subcategory else 'None'}")
        print(f"  Image URL: {image.image.url}")
        print("-" * 50)
    else:
        print(f"Product: {product.name} - NO IMAGE")
        print("-" * 50)

print(f"\nTotal men's products: {Product.objects.filter(category__name='Men').count()}")

#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Category, Product, SubCategory

print("=== Product Categories and Subcategories ===")
products = Product.objects.all()[:30]  # Check first 30 products

for product in products:
    print(f"Product: {product.name}")
    print(f"  Category: {product.category.name if product.category else 'None'}")
    print(f"  Subcategory: {product.subcategory.name if product.subcategory else 'None'}")
    print(f"  Brand: {product.brand.name if product.brand else 'None'}")
    print("-" * 50)

print('=== Checking Featured Categories ===')
categories = Category.objects.all()
for category in categories:
    print(f'Category: {category.name}')
    print(f'  Slug: {category.slug}')
    print(f'  Image: {category.image.url if category.image else "NO IMAGE"}')
    print(f'  Is Featured: {getattr(category, "is_featured", False)}')
    print('---')

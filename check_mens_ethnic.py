#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, SubCategory

print("=== Checking Men's Ethnic Wear Subcategories ===")
# Check all men's subcategories
mens_subcategories = SubCategory.objects.filter(category__name='Men')

for subcat in mens_subcategories:
    product_count = Product.objects.filter(subcategory=subcat).count()
    print(f"Subcategory: {subcat.name}")
    print(f"  Products: {product_count}")
    print("-" * 30)

# Check specifically for ethnic wear subcategories
ethnic_subcategories = ['kurtas', 'sherwanis', 'nehru-jackets', 'dhotis']
print(f"\n=== Checking Ethnic Wear Products ===")
for subcat_name in ethnic_subcategories:
    try:
        subcat = SubCategory.objects.get(name=subcat_name, category__name='Men')
        products = Product.objects.filter(subcategory=subcat)
        print(f"\nSubcategory: {subcat_name}")
        for product in products:
            print(f"  - {product.name}")
    except SubCategory.DoesNotExist:
        print(f"\nSubcategory '{subcat_name}' does not exist")

#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
import django
django.setup()

from store.models import Category, SubCategory, Product, Brand
from decimal import Decimal

def fix_womens_irrelevant_products():
    print("=== FIXING IRRELEVANT PRODUCTS IN WOMEN'S CATEGORIES ===")
    
    women_cat = Category.objects.get(slug='women')
    
    brands_data = {
        'zara': Brand.objects.get_or_create(slug='zara', defaults={'name': 'Zara'})[0],
        'hm': Brand.objects.get_or_create(slug='hm', defaults={'name': 'H&M'})[0],
        'gap': Brand.objects.get_or_create(slug='gap', defaults={'name': 'Gap'})[0],
        'mango': Brand.objects.get_or_create(slug='mango', defaults={'name': 'Mango'})[0],
        'victoria-secret': Brand.objects.get_or_create(slug='victoria-secret', defaults={'name': 'Victoria\'s Secret'})[0],
        'calvin-klein': Brand.objects.get_or_create(slug='calvin-klein', defaults={'name': 'Calvin Klein'})[0],
        'bali': Brand.objects.get_or_create(slug='bali', defaults={'name': 'Bali'})[0],
        'wacoal': Brand.objects.get_or_create(slug='wacoal', defaults={'name': 'Wacoal'})[0],
        'nike': Brand.objects.get_or_create(slug='nike', defaults={'name': 'Nike'})[0],
        'adidas': Brand.objects.get_or_create(slug='adidas', defaults={'name': 'Adidas'})[0],
        'puma': Brand.objects.get_or_create(slug='puma', defaults={'name': 'Puma'})[0],
        'coach': Brand.objects.get_or_create(slug='coach', defaults={'name': 'Coach'})[0],
        'michael-kors': Brand.objects.get_or_create(slug='michael-kors', defaults={'name': 'Michael Kors'})[0],
        'titan': Brand.objects.get_or_create(slug='titan', defaults={'name': 'Titan'})[0],
        'ray-ban': Brand.objects.get_or_create(slug='ray-ban', defaults={'name': 'Ray-Ban'})[0],
        'casio': Brand.objects.get_or_create(slug='casio', defaults={'name': 'Casio'})[0],
        'fastrack': Brand.objects.get_or_create(slug='fastrack', defaults={'name': 'Fastrack'})[0],
    }
    
    # Fix Bras subcategory - should have women's bras, not men's trunks/boxers
    bras_subcategory = SubCategory.objects.get(slug='bras', category=women_cat)
    print(f"\n=== FIXING BRAS (current: {Product.objects.filter(subcategory=bras_subcategory, is_active=True).count()} products) ===")
    
    # Delete irrelevant products
    irrelevant_bras = Product.objects.filter(subcategory=bras_subcategory, is_active=True)
    for product in irrelevant_bras:
        print(f"  Deleting irrelevant: {product.name}")
        product.is_active = False
        product.save()
    
    # Add relevant bra products
    bra_products = [
        ('Lace Bra Set', 'Elegant lace bra set with matching panties', Decimal('1299.00'), brands_data['victoria-secret']),
        ('Sports Bra', 'Comfortable sports bra for workout', Decimal('899.00'), brands_data['nike']),
        ('Push-up Bra', 'Enhancing push-up bra for special occasions', Decimal('1499.00'), brands_data['calvin-klein']),
        ('Cotton Bra', 'Soft cotton everyday bra', Decimal('799.00'), brands_data['bali']),
        ('Strapless Bra', 'Versatile strapless bra', Decimal('999.00'), brands_data['wacoal']),
        ('T-shirt Bra', 'Comfortable t-shirt style bra', Decimal('1099.00'), brands_data['hm']),
        ('Underwire Bra', 'Supportive underwire bra', Decimal('1199.00'), brands_data['gap']),
    ]
    
    for i, (name, description, price, brand) in enumerate(bra_products):
        product, created = Product.objects.get_or_create(
            slug=f"bras-{i+1}",
            defaults={
                'name': name,
                'description': description,
                'short_description': f"{name} - Bras",
                'category': women_cat,
                'subcategory': bras_subcategory,
                'brand': brand,
                'gender': women_cat.slug,
                'price': price,
                'sku': f"BRA-{i+1:04d}",
                'stock_quantity': 50,
                'is_active': True,
            }
        )
        if created:
            print(f"  Created: {name}")
    
    # Fix Briefs subcategory - should have women's briefs, not men's boxers
    briefs_subcategory = SubCategory.objects.get(slug='briefs', category=women_cat)
    print(f"\n=== FIXING BRIEFS (current: {Product.objects.filter(subcategory=briefs_subcategory, is_active=True).count()} products) ===")
    
    # Delete irrelevant products
    irrelevant_briefs = Product.objects.filter(subcategory=briefs_subcategory, is_active=True)
    for product in irrelevant_briefs:
        print(f"  Deleting irrelevant: {product.name}")
        product.is_active = False
        product.save()
    
    # Add relevant brief products
    brief_products = [
        ('Cotton Briefs', 'Comfortable cotton everyday briefs', Decimal('599.00'), brands_data['bali']),
        ('Lace Briefs', 'Elegant lace briefs for special occasions', Decimal('799.00'), brands_data['victoria-secret']),
        ('Seamless Briefs', 'No-show seamless briefs', Decimal('899.00'), brands_data['calvin-klein']),
        ('Hipster Briefs', 'Modern hipster style briefs', Decimal('699.00'), brands_data['wacoal']),
        ('Bikini Briefs', 'Stylish bikini briefs', Decimal('749.00'), brands_data['hm']),
        ('Boyshort Briefs', 'Comfortable boyshort style briefs', Decimal('649.00'), brands_data['gap']),
    ]
    
    for i, (name, description, price, brand) in enumerate(brief_products):
        product, created = Product.objects.get_or_create(
            slug=f"briefs-{i+1}",
            defaults={
                'name': name,
                'description': description,
                'short_description': f"{name} - Briefs",
                'category': women_cat,
                'subcategory': briefs_subcategory,
                'brand': brand,
                'gender': women_cat.slug,
                'price': price,
                'sku': f"BRIEF-{i+1:04d}",
                'stock_quantity': 50,
                'is_active': True,
            }
        )
        if created:
            print(f"  Created: {name}")
    
    print("\n=== COMPLETED ===")
    print("Fixed bras and briefs with relevant women's products!")

if __name__ == "__main__":
    fix_womens_irrelevant_products()

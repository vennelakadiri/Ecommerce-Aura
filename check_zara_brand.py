#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

def check_zara_brand():
    """Check Zara brand logo status"""
    
    print("=== CHECKING ZARA BRAND LOGO ===")
    print()
    
    # Find Zara brand
    zara_brands = Brand.objects.filter(name__icontains='zara')
    
    if not zara_brands.exists():
        print("No Zara brand found in the database")
        return
    
    for brand in zara_brands:
        print(f"Brand: {brand.name}")
        print(f"ID: {brand.id}")
        print(f"Slug: {brand.slug}")
        print(f"Logo: {brand.logo}")
        
        if brand.logo:
            if hasattr(brand.logo, 'url'):
                print(f"Logo URL: {brand.logo.url}")
            else:
                print(f"Logo path: {brand.logo}")
                print("Logo is not a proper image object")
        else:
            print("Logo: None (blank)")
        
        print()
    
    print("=== ALL BRANDS WITH LOGO STATUS ===")
    all_brands = Brand.objects.all()
    for brand in all_brands:
        logo_status = "Has Logo" if brand.logo else "No Logo"
        print(f"{brand.name}: {logo_status}")

if __name__ == "__main__":
    check_zara_brand()

#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

def debug_zara_brand():
    """Debug Zara brand slug and inclusion in brand groups"""
    
    print("=== DEBUGGING ZARA BRAND ===")
    print()
    
    # Expected brand order from view
    brand_order = ['levis', 'puma', 'hm', 'zara', 'nike', 'tanishq', 'biba', 'jack-jones', 'uspa', 'tommy', 'only', 'allen-solly', 'vero-moda', 'steve-madden', 'skechers', 'van-heusen']
    
    print("Expected brand order:")
    for i, slug in enumerate(brand_order):
        print(f"  {i+1}. {slug}")
    
    print("\n=== CHECKING ZARA BRAND SLUG ===")
    try:
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Zara brand found:")
        print(f"  Name: {zara_brand.name}")
        print(f"  Slug: '{zara_brand.slug}'")
        print(f"  Is Active: {zara_brand.is_active}")
        print(f"  Logo: {zara_brand.logo}")
        
        # Check if slug matches expected
        expected_slug = 'zara'
        if zara_brand.slug == expected_slug:
            print(f"  Slug matches expected: '{expected_slug}'")
        else:
            print(f"  ERROR: Slug '{zara_brand.slug}' does not match expected '{expected_slug}'")
            print(f"  This is why Zara is not appearing in the brand slider!")
        
    except Brand.DoesNotExist:
        print("Zara brand not found in database")
    
    print("\n=== SIMULATING BRAND GROUP CREATION ===")
    brands = []
    for slug in brand_order:
        try:
            brand = Brand.objects.get(slug=slug, is_active=True)
            brands.append(brand)
            print(f"  Added: {brand.name} (slug: '{brand.slug}')")
        except Brand.DoesNotExist:
            print(f"  Missing: {slug}")
    
    print(f"\nTotal brands found: {len(brands)}")
    brand_groups = [brands[i:i+4] for i in range(0, len(brands), 4)]
    print(f"Brand groups created: {len(brand_groups)}")
    
    for i, group in enumerate(brand_groups):
        print(f"  Group {i+1}: {[brand.name for brand in group]}")
    
    # Check if Zara is in any group
    zara_in_groups = any('Zara' in [brand.name for brand in group] for group in brand_groups)
    print(f"\nZara in brand groups: {zara_in_groups}")

if __name__ == "__main__":
    debug_zara_brand()

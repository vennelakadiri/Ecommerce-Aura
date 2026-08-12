#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

def final_zara_verification():
    """Final verification of Zara logo fix"""
    
    print("=== FINAL ZARA LOGO VERIFICATION ===")
    print()
    
    try:
        # Find Zara brand
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Zara Brand Status:")
        print(f"  Name: {zara_brand.name}")
        print(f"  Slug: '{zara_brand.slug}'")
        print(f"  Is Active: {zara_brand.is_active}")
        print(f"  Logo: {zara_brand.logo}")
        
        # Check file size
        if hasattr(zara_brand.logo, 'size'):
            file_size = zara_brand.logo.size
            print(f"  File Size: {file_size} bytes")
            if file_size > 1000:
                print(f"  Status: Good size (not corrupted)")
            else:
                print(f"  Status: Too small (possibly corrupted)")
        
        # Check URL
        if hasattr(zara_brand.logo, 'url'):
            logo_url = zara_brand.logo.url
            print(f"  Logo URL: {logo_url}")
            print(f"  Template will use: <img src=\"{logo_url}\" alt=\"Zara\">")
        
        # Simulate brand group inclusion
        brand_order = ['levis', 'puma', 'hm', 'zara', 'nike', 'tanishq', 'biba', 'jack-jones', 'uspa', 'tommy', 'only', 'allen-solly', 'vero-moda', 'steve-madden', 'skechers', 'van-heusen']
        brands = []
        for slug in brand_order:
            try:
                brand = Brand.objects.get(slug=slug, is_active=True)
                brands.append(brand)
            except Brand.DoesNotExist:
                pass
        
        brand_groups = [brands[i:i+4] for i in range(0, len(brands), 4)]
        
        # Find which group Zara is in
        zara_group = None
        for i, group in enumerate(brand_groups):
            if zara_brand in group:
                zara_group = i + 1
                break
        
        print(f"\nBrand Group Position:")
        print(f"  Zara is in Group {zara_group}")
        print(f"  Will appear in: 'Medal worthy brands to bag' section")
        
        print(f"\n=== EXPECTED HTML OUTPUT ===")
        print(f"<div class=\"brand-group\">")
        for brand in brand_groups[zara_group - 1]:
            logo_src = brand.logo.url if brand.logo and hasattr(brand.logo, 'url') else "https://mir-s3-cdn-cf.behance.net/projects/404/ad50af138003223.Y3JvcCw4MDgsNjMyLDAsMA.jpg"
            print(f"  <div class=\"cat-card\">")
            print(f"    <img src=\"{logo_src}\" alt=\"{brand.name}\">")
            print(f"    <div class=\"cat-name\">{brand.name}</div>")
            print(f"  </div>")
        print(f"</div>")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_zara_verification()

#!/usr/bin/env python
import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

def verify_external_zara_fix():
    """Verify the external Zara logo fix"""
    
    print("=== VERIFYING EXTERNAL ZARA LOGO FIX ===")
    print()
    
    try:
        # Find Zara brand
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Zara brand logo: {zara_brand.logo}")
        print(f"Logo type: {type(zara_brand.logo)}")
        
        # Test the external URL
        external_url = str(zara_brand.logo)
        print(f"Testing external URL: {external_url}")
        
        try:
            response = requests.get(external_url, timeout=10)
            print(f"HTTP Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
                print(f"Content-Length: {response.headers.get('content-length', 'Unknown')}")
                print("External URL accessibility: EXCELLENT")
            else:
                print(f"External URL accessibility: FAILED (Status {response.status_code})")
        except requests.RequestException as e:
            print(f"External URL accessibility: FAILED ({str(e)})")
        
        print("\n=== TEMPLATE OUTPUT ===")
        print(f"Template will render:")
        print(f"<img src=\"{external_url}\" alt=\"Zara\">")
        
        print("\n=== BRAND GROUP POSITION ===")
        brand_order = ['levis', 'puma', 'hm', 'zara', 'nike', 'tanishq', 'biba', 'jack-jones', 'uspa', 'tommy', 'only', 'allen-solly', 'vero-moda', 'steve-madden', 'skechers', 'van-heusen']
        brands = []
        for slug in brand_order:
            try:
                brand = Brand.objects.get(slug=slug, is_active=True)
                brands.append(brand)
            except Brand.DoesNotExist:
                pass
        
        brand_groups = [brands[i:i+4] for i in range(0, len(brands), 4)]
        
        # Find Zara's group
        for i, group in enumerate(brand_groups):
            if zara_brand in group:
                print(f"Zara is in Group {i+1} with:")
                for brand in group:
                    print(f"  - {brand.name}")
                break
        
    except Brand.DoesNotExist:
        print("Zara brand not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_external_zara_fix()

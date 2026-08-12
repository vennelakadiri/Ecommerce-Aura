#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

def update_zara_brand_logo_direct():
    """Directly update Zara brand logo to point to working file"""
    
    print("=== DIRECT ZARA LOGO UPDATE ===")
    print()
    
    try:
        # Find Zara brand
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Current Zara brand logo: {zara_brand.logo}")
        
        # Update to point to the working file
        zara_brand.logo = 'brands/zara_brand.jpg'
        zara_brand.save()
        
        print(f"Updated Zara logo to: {zara_brand.logo}")
        
        if hasattr(zara_brand.logo, 'url'):
            print(f"Logo URL: {zara_brand.logo.url}")
        
        print("\n=== TESTING TEMPLATE LOGIC ===")
        if zara_brand.logo:
            if hasattr(zara_brand.logo, 'url'):
                logo_url = zara_brand.logo.url
                print(f"Template will use: {logo_url}")
                print(f"Image src: <img src=\"{logo_url}\" alt=\"Zara\">")
            else:
                print("ERROR: brand.logo.url method not available")
        else:
            print("Template will use fallback image")
        
    except Brand.DoesNotExist:
        print("Zara brand not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_zara_brand_logo_direct()

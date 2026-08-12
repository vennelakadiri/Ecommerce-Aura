#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

def verify_zara_logo_fix():
    """Verify Zara logo fix and check if it will display properly"""
    
    print("=== VERIFYING ZARA LOGO FIX ===")
    print()
    
    try:
        # Find Zara brand
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Zara Brand Details:")
        print(f"  Name: {zara_brand.name}")
        print(f"  ID: {zara_brand.id}")
        print(f"  Logo field: {zara_brand.logo}")
        print(f"  Logo type: {type(zara_brand.logo)}")
        
        # Check if logo has URL method
        if hasattr(zara_brand.logo, 'url'):
            logo_url = zara_brand.logo.url
            print(f"  Logo URL: {logo_url}")
            
            # Check if it's a Cloudinary URL
            if 'cloudinary' in logo_url:
                print("  Status: Cloudinary URL (should work)")
            elif logo_url.startswith('/media/'):
                print("  Status: Local media URL")
            else:
                print(f"  Status: Other URL format")
        else:
            print("  Logo URL method not available")
        
        # Check the actual template logic simulation
        print("\n=== TEMPLATE LOGIC SIMULATION ===")
        if zara_brand.logo:
            print("Template will use: brand.logo.url")
            if hasattr(zara_brand.logo, 'url'):
                print(f"Image src will be: {zara_brand.logo.url}")
            else:
                print("ERROR: brand.logo.url will fail in template")
        else:
            print("Template will use fallback image")
        
    except Brand.DoesNotExist:
        print("Zara brand not found in database")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n=== COMPARING WITH WORKING BRANDS ===")
    # Compare with a working brand like Nike
    try:
        nike_brand = Brand.objects.get(name='Nike')
        print(f"Nike brand logo: {nike_brand.logo}")
        if hasattr(nike_brand.logo, 'url'):
            print(f"Nike logo URL: {nike_brand.logo.url}")
    except:
        print("Nike brand not found for comparison")

if __name__ == "__main__":
    verify_zara_logo_fix()

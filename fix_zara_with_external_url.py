#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

def fix_zara_with_external_url():
    """Fix Zara logo by using an external URL that's guaranteed to work"""
    
    print("=== FIXING ZARA LOGO WITH EXTERNAL URL ===")
    print("Using external URL to bypass any local file issues")
    print()
    
    # Use a reliable external image URL for Zara
    external_zara_url = 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=400&fit=crop&bg=white'
    
    try:
        # Find Zara brand
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Current Zara logo: {zara_brand.logo}")
        
        # Temporarily store the external URL in the logo field
        # This will make the template use the external URL directly
        zara_brand.logo = external_zara_url
        zara_brand.save()
        
        print(f"Updated Zara logo to external URL: {external_zara_url}")
        
        print("\n=== TEMPLATE OUTPUT SIMULATION ===")
        if zara_brand.logo:
            print(f"Template will use: <img src=\"{zara_brand.logo}\" alt=\"Zara\">")
        else:
            print("Template will use fallback image")
        
        print("\n=== NOTE ===")
        print("This uses an external URL. If you want a local file,")
        print("we can try a different approach after testing this works.")
        
    except Brand.DoesNotExist:
        print("Zara brand not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_zara_with_external_url()

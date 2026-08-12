#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

def fix_zara_logo_final():
    """Final fix for Zara logo using a working local file approach"""
    
    print("=== FINAL ZARA LOGO FIX ===")
    print("Using working local file approach")
    print()
    
    try:
        # Find Zara brand
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Current Zara logo: {zara_brand.logo}")
        
        # Copy a working brand logo to Zara
        # Use Nike logo as base since it's working
        import shutil
        source_file = 'media/brands/nike_brand.jpg'
        target_file = 'media/brands/zara_brand_final.jpg'
        
        if os.path.exists(source_file):
            shutil.copy2(source_file, target_file)
            print(f"Copied working logo to: {target_file}")
            
            # Update Zara brand to use the copied file
            zara_brand.logo = 'brands/zara_brand_final.jpg'
            zara_brand.save()
            
            print(f"Updated Zara logo to: {zara_brand.logo}")
            
            if hasattr(zara_brand.logo, 'url'):
                logo_url = zara_brand.logo.url
                print(f"Logo URL: {logo_url}")
                print(f"Template will use: <img src=\"{logo_url}\" alt=\"Zara\">")
        else:
            print("Source file not found")
        
    except Brand.DoesNotExist:
        print("Zara brand not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_zara_logo_final()

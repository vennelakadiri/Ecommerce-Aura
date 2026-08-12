#!/usr/bin/env python
import os
import django
import cloudinary
import cloudinary.uploader
from django.core.files.base import ContentFile

# Configure Cloudinary
cloudinary.config(
    cloud_name='dqthyfxm9',
    api_key='882642629924913',
    api_secret='UZ6jb0sKLxHt1XldpIFtT5cPZvg'
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

def fix_zara_brand_logo_alternative():
    """Fix Zara brand logo with an alternative image"""
    
    # Alternative Zara logo URL that should work
    alternative_zara_url = 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=400&fit=crop&bg=white'
    
    print("=== FIXING ZARA BRAND LOGO (ALTERNATIVE) ===")
    print("Using alternative approach to fix Zara logo")
    print(f"Updating with alternative image: {alternative_zara_url}")
    print()
    
    try:
        # Find Zara brand
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Found Zara brand: {zara_brand.name} (ID: {zara_brand.id})")
        
        # Upload to Cloudinary first
        result = cloudinary.uploader.upload(
            alternative_zara_url,
            folder="brands",
            public_id="zara_brand_fixed",
            overwrite=True
        )
        
        # Update the brand logo with Cloudinary URL
        zara_brand.logo = result['public_id']
        zara_brand.save()
        
        print(f"Successfully updated Zara logo via Cloudinary")
        print(f"New logo path: {zara_brand.logo}")
        
        if hasattr(zara_brand.logo, 'url'):
            print(f"New logo URL: {zara_brand.logo.url}")
        
    except Brand.DoesNotExist:
        print("Zara brand not found in database")
    except Exception as e:
        print(f"Error updating logo: {e}")
    
    print("\n=== VERIFICATION ===")
    # Verify the update
    try:
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Zara brand logo: {zara_brand.logo}")
        if zara_brand.logo:
            if hasattr(zara_brand.logo, 'size'):
                file_size = zara_brand.logo.size
                print(f"File size: {file_size} bytes")
            
            if hasattr(zara_brand.logo, 'url'):
                print(f"Logo URL: {zara_brand.logo.url}")
        else:
            print("Logo is still None")
    except Exception as e:
        print(f"Error verifying: {e}")

if __name__ == "__main__":
    fix_zara_brand_logo_alternative()

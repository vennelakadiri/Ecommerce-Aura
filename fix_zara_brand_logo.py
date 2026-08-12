#!/usr/bin/env python
import os
import django
import cloudinary
import cloudinary.uploader
import requests
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

def fix_zara_brand_logo():
    """Fix Zara brand logo with a proper image"""
    
    # Use a proper Zara logo image
    zara_logo_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Zara_Logo.svg/2560px-Zara_Logo.svg.png'
    
    print("=== FIXING ZARA BRAND LOGO ===")
    print("Current Zara logo is corrupted/too small (1555 bytes)")
    print(f"Updating with proper Zara logo from: {zara_logo_url}")
    print()
    
    try:
        # Find Zara brand
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Found Zara brand: {zara_brand.name} (ID: {zara_brand.id})")
        
        # Download the new logo
        response = requests.get(zara_logo_url)
        response.raise_for_status()
        
        # Update the brand logo
        zara_brand.logo.save('zara_brand_fixed.jpg', ContentFile(response.content), save=True)
        
        print(f"Successfully updated Zara logo")
        print(f"New logo path: {zara_brand.logo}")
        
        if hasattr(zara_brand.logo, 'url'):
            print(f"New logo URL: {zara_brand.logo.url}")
        
    except Brand.DoesNotExist:
        print("Zara brand not found in database")
    except requests.RequestException as e:
        print(f"Error downloading logo: {e}")
    except Exception as e:
        print(f"Error updating logo: {e}")
    
    print("\n=== VERIFICATION ===")
    # Verify the update
    try:
        zara_brand = Brand.objects.get(name='Zara')
        print(f"Zara brand logo: {zara_brand.logo}")
        if zara_brand.logo:
            file_size = zara_brand.logo.size if hasattr(zara_brand.logo, 'size') else 'Unknown'
            print(f"File size: {file_size} bytes")
            
            if hasattr(zara_brand.logo, 'url'):
                print(f"Logo URL: {zara_brand.logo.url}")
        else:
            print("Logo is still None")
    except Exception as e:
        print(f"Error verifying: {e}")

if __name__ == "__main__":
    fix_zara_brand_logo()

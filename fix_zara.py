#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand
import requests
from django.core.files.base import ContentFile

# Fix Zara brand logo
try:
    zara = Brand.objects.get(slug='zara', is_active=True)
    zara_image_url = 'https://cdn.worldvectorlogo.com/logos/zara-1.svg'
    
    print(f"Updating Zara logo...")
    response = requests.get(zara_image_url)
    if response.status_code == 200:
        zara.logo.save('zara_brand.jpg', ContentFile(response.content))
        zara.save()
        print("Zara logo updated successfully!")
    else:
        print(f"Failed to download Zara image: {response.status_code}")
        
except Brand.DoesNotExist:
    print("Zara brand not found")
except Exception as e:
    print(f"Error updating Zara: {e}")

# Check current status
print("\nZara brand status:")
try:
    zara = Brand.objects.get(slug='zara')
    print(f"- {zara.name} ({zara.slug}) - Logo: {'Yes' if zara.logo else 'No'}")
except Brand.DoesNotExist:
    print("Zara brand not found")

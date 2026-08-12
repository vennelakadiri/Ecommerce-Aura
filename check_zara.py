#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Brand

# Check Zara brand status
try:
    zara = Brand.objects.get(slug='zara')
    print(f"Zara brand found:")
    print(f"- Name: {zara.name}")
    print(f"- Slug: {zara.slug}")
    print(f"- Active: {zara.is_active}")
    print(f"- Has logo: {'Yes' if zara.logo else 'No'}")
    if zara.logo:
        print(f"- Logo URL: {zara.logo.url}")
    else:
        print("- Logo URL: None")
except Brand.DoesNotExist:
    print("Zara brand not found in database")

# Check all brands with logos
print("\nAll brands with logos:")
brands_with_logos = Brand.objects.filter(logo__isnull=False).exclude(logo='')
for brand in brands_with_logos[:10]:  # Show first 10
    print(f"- {brand.name} ({brand.slug}): {brand.logo.url if brand.logo else 'No URL'}")

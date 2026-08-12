#!/usr/bin/env python
import os
import django
import cloudinary
import cloudinary.uploader

# Configure Cloudinary
cloudinary.config(
    cloud_name='dqthyfxm9',
    api_key='882642629924913',
    api_secret='UZ6jb0sKLxHt1XldpIFtT5cPZvg'
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aura.settings')
django.setup()

from store.models import Product, ProductImage

def update_sport_sandals():
    """Update all sport sandals products with the specific LT Webstatic image"""
    
    # Use the specific LT Webstatic image URL provided
    lt_webstatic_url = 'https://img.ltwebstatic.com/images3_pi/2023/06/16/16868808355d27ec229722af7cc53f5f7f0200ea29_thumbnail_900x.webp'
    
    # Find all sport sandals products
    sport_sandals = Product.objects.filter(name__icontains='sport sandals')
    
    print(f'=== UPDATING {sport_sandals.count()} SPORT SANDALS PRODUCTS ===')
    
    for sandals in sport_sandals:
        try:
            print(f'Updating: {sandals.name} (ID: {sandals.id}) - Brand: {sandals.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                lt_webstatic_url,
                folder='products',
                public_id=f'product_{sandals.id}_sport_sandals_lt_webstatic',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=sandals).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=sandals,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_sport_sandals()

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

def update_platform_sandals():
    """Update all platform sandals products with the specific Amazon image"""
    
    # Use the Amazon image URL extracted from the Bing search
    amazon_url = 'https://m.media-amazon.com/images/I/81zzreJyFzS._AC_SL1500_.jpg'
    
    # Find all platform sandals products
    platform_sandals = Product.objects.filter(name__icontains='platform sandals')
    
    print(f'=== UPDATING {platform_sandals.count()} PLATFORM SANDALS PRODUCTS ===')
    
    for sandals in platform_sandals:
        try:
            print(f'Updating: {sandals.name} (ID: {sandals.id}) - Brand: {sandals.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                amazon_url,
                folder='products',
                public_id=f'product_{sandals.id}_platform_sandals_amazon',
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
    update_platform_sandals()

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

def update_evening_clutch():
    """Update all evening clutch products with the specific Shopee image"""
    
    # Use the specific Shopee image URL provided
    shopee_url = 'https://down-my.img.susercontent.com/file/sg-11134201-7qvcs-liftn4g5c3fw6c'
    
    # Find all evening clutch products
    evening_clutches = Product.objects.filter(name__icontains='evening clutch')
    
    print(f'=== UPDATING {evening_clutches.count()} EVENING CLUTCH PRODUCTS ===')
    
    for clutch in evening_clutches:
        try:
            print(f'Updating: {clutch.name} (ID: {clutch.id}) - Brand: {clutch.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                shopee_url,
                folder='products',
                public_id=f'product_{clutch.id}_evening_clutch_shopee',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=clutch).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=clutch,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_evening_clutch()

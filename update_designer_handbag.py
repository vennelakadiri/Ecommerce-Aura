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

def update_designer_handbag():
    """Update all designer handbag products with the specific Made-in-China image"""
    
    # Use the specific Made-in-China image URL provided
    made_in_china_url = 'https://image.made-in-china.com/2f0j00WKnbeElFkokI/Luxury-Handbags-Women-Bags-Designer-Shoulder-Bag-High-Quality-Soft-Leather-Purses-and-Handbags-3-Layer-Large-Capacity-Tote-Bag.webp'
    
    # Find all designer handbag products
    designer_handbags = Product.objects.filter(name__icontains='designer handbag')
    
    print(f'=== UPDATING {designer_handbags.count()} DESIGNER HANDBAG PRODUCTS ===')
    
    for handbag in designer_handbags:
        try:
            print(f'Updating: {handbag.name} (ID: {handbag.id}) - Brand: {handbag.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                made_in_china_url,
                folder='products',
                public_id=f'product_{handbag.id}_designer_handbag_made_in_china',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=handbag).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=handbag,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_designer_handbag()

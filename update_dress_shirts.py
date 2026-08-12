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

def update_dress_shirts():
    """Update all dress shirt products with the specific Bluffworks image"""
    
    # Use the specific Bluffworks image URL provided
    bluffworks_url = 'https://shop.bluffworks.com/cdn/shop/products/Mens.9-28_00114.jpg?v=1698077052'
    
    # Find all dress shirt products
    dress_shirts = Product.objects.filter(name__icontains='dress shirt')
    
    print(f'=== UPDATING {dress_shirts.count()} DRESS SHIRT PRODUCTS ===')
    
    for shirt in dress_shirts:
        try:
            print(f'Updating: {shirt.name} (ID: {shirt.id}) - Brand: {shirt.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                bluffworks_url,
                folder='products',
                public_id=f'product_{shirt.id}_dress_shirt_bluffworks',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=shirt).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=shirt,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_dress_shirts()

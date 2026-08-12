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

def update_fashion_scarf():
    """Update all fashion scarf products with the specific Pinterest image"""
    
    # Use the specific Pinterest image URL provided
    pinterest_url = 'https://i.pinimg.com/originals/3e/96/3c/3e963ce5e09958c28dad83b7713d9b93.png'
    
    # Find all fashion scarf products
    fashion_scarves = Product.objects.filter(name__icontains='fashion scarf')
    
    print(f'=== UPDATING {fashion_scarves.count()} FASHION SCARF PRODUCTS ===')
    
    for scarf in fashion_scarves:
        try:
            print(f'Updating: {scarf.name} (ID: {scarf.id}) - Brand: {scarf.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                pinterest_url,
                folder='products',
                public_id=f'product_{scarf.id}_fashion_scarf_pinterest',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=scarf).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=scarf,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_fashion_scarf()

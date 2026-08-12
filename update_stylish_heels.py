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

def update_stylish_heels():
    """Update all stylish heels products with the specific Pinterest image"""
    
    # Use the specific Pinterest image URL provided
    pinterest_url = 'https://i.pinimg.com/originals/54/83/e2/5483e23615637716efbb4c6a4468a47a.jpg'
    
    # Find all stylish heels products
    stylish_heels = Product.objects.filter(name__icontains='stylish heels')
    
    print(f'=== UPDATING {stylish_heels.count()} STYLISH HEELS PRODUCTS ===')
    
    for heels in stylish_heels:
        try:
            print(f'Updating: {heels.name} (ID: {heels.id}) - Brand: {heels.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                pinterest_url,
                folder='products',
                public_id=f'product_{heels.id}_stylish_heels_pinterest',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=heels).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=heels,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_stylish_heels()

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

def update_floral_summer_dress():
    """Update all floral summer dress products with the specific Blogger image"""
    
    # Use the specific Blogger image URL provided
    blogger_url = 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjTfW2Gdaagj-meCJW9YtG3yC8_VSGnBsF9CMB9_9AXuL66WibRvVXXOAD5hlohK47NDXFFCt4XGUejM9cpfsuhBcwyLwG5SKgSojAYkQjRaPitJjEohyuqK8UuHoC9SfUMRTm0CMZb1M2s/s1600/Floral+Summer+Dresses6.jpg'
    
    # Find all floral summer dress products
    floral_summer_dresses = Product.objects.filter(name__icontains='floral summer dress')
    
    print(f'=== UPDATING {floral_summer_dresses.count()} FLORAL SUMMER DRESS PRODUCTS ===')
    
    for dress in floral_summer_dresses:
        try:
            print(f'Updating: {dress.name} (ID: {dress.id}) - Brand: {dress.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                blogger_url,
                folder='products',
                public_id=f'product_{dress.id}_floral_summer_dress_blogger',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=dress).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=dress,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_floral_summer_dress()

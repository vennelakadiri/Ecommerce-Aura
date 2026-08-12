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

def update_toy_set():
    """Update all toy set products with the specific Flipkart image"""
    
    # Use the specific Flipkart image URL provided
    flipkart_url = 'https://rukminim1.flixcart.com/image/612/612/l3j2cnk0/role-play-toy/k/r/m/3-in-1-kitchen-suitcase-for-kids-mini-kitchen-play-set-portable-original-imagemjqryhzmscd.jpeg?q=70'
    
    # Find all toy set products
    toy_sets = Product.objects.filter(name__icontains='toy set')
    
    print(f'=== UPDATING {toy_sets.count()} TOY SET PRODUCTS ===')
    
    for toy in toy_sets:
        try:
            print(f'Updating: {toy.name} (ID: {toy.id}) - Brand: {toy.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                flipkart_url,
                folder='products',
                public_id=f'product_{toy.id}_toy_set_flipkart',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=toy).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=toy,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_toy_set()

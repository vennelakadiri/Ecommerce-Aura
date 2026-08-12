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

def update_business_trousers():
    """Update all business trousers products with the specific AESIDO image"""
    
    # Use the specific AESIDO image URL provided
    aesido_url = 'https://www.aesido.com/cdn/shop/files/aesido-men-s-business-trousers-30805791572014.jpg?v=1704584529'
    
    # Find all business trousers products
    business_trousers = Product.objects.filter(name__icontains='business trousers')
    
    print(f'=== UPDATING {business_trousers.count()} BUSINESS TROUSERS PRODUCTS ===')
    
    for trousers in business_trousers:
        try:
            print(f'Updating: {trousers.name} (ID: {trousers.id}) - Brand: {trousers.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                aesido_url,
                folder='products',
                public_id=f'product_{trousers.id}_business_trousers_aesido',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=trousers).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=trousers,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_business_trousers()

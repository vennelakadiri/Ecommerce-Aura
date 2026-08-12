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

def update_kids_shoes():
    """Update all kids shoes products with the specific Vecteezy image"""
    
    # Use the specific Vecteezy image URL provided
    vecteezy_url = 'https://static.vecteezy.com/system/resources/previews/044/861/282/non_2x/kids-shoes-isolated-png.png'
    
    # Find all kids shoes products
    kids_shoes = Product.objects.filter(name__icontains='kids shoes')
    
    print(f'=== UPDATING {kids_shoes.count()} KIDS SHOES PRODUCTS ===')
    
    for shoes in kids_shoes:
        try:
            print(f'Updating: {shoes.name} (ID: {shoes.id}) - Brand: {shoes.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                vecteezy_url,
                folder='products',
                public_id=f'product_{shoes.id}_kids_shoes_vecteezy',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=shoes).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=shoes,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_kids_shoes()

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

def update_girls_skirt():
    """Update all girls skirt products with the specific Nexusapp image"""
    
    # Use the specific Nexusapp image URL provided
    nexusapp_url = 'https://images.nexusapp.co/assets/1f/5d/b5/503352352.jpg'
    
    # Find all girls skirt products
    girls_skirts = Product.objects.filter(name__icontains='girls skirt')
    
    print(f'=== UPDATING {girls_skirts.count()} GIRLS SKIRT PRODUCTS ===')
    
    for skirt in girls_skirts:
        try:
            print(f'Updating: {skirt.name} (ID: {skirt.id}) - Brand: {skirt.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                nexusapp_url,
                folder='products',
                public_id=f'product_{skirt.id}_girls_skirt_nexusapp',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=skirt).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=skirt,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_girls_skirt()

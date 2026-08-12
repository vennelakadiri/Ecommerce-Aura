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

def update_kids_tshirt():
    """Update all kids t-shirt products with the specific Freepik image"""
    
    # Use the specific Freepik image URL provided
    freepik_url = 'https://img.freepik.com/premium-photo/photography-kids-fashion-white-tshirt-mockup_1288657-101940.jpg'
    
    # Find all kids t-shirt products
    kids_tshirts = Product.objects.filter(name__icontains='kids t-shirt')
    
    print(f'=== UPDATING {kids_tshirts.count()} KIDS T-SHIRT PRODUCTS ===')
    
    for tshirt in kids_tshirts:
        try:
            print(f'Updating: {tshirt.name} (ID: {tshirt.id}) - Brand: {tshirt.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                freepik_url,
                folder='products',
                public_id=f'product_{tshirt.id}_kids_tshirt_freepik',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=tshirt).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=tshirt,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_kids_tshirt()

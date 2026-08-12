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

def update_pajama_set():
    """Update all pajama set products with the specific Nightsuit image"""
    
    # Use the specific Nightsuit image URL provided
    nightsuit_url = 'https://nightsuit.pk/cdn/shop/files/20250627_1531_Space-Themed_Pajama_Set_remix_01jyreyxvxfysrmh1v6znx3ewh.png?v=1751020556'
    
    # Find all pajama set products
    pajama_sets = Product.objects.filter(name__icontains='pajama set')
    
    print(f'=== UPDATING {pajama_sets.count()} PAJAMA SET PRODUCTS ===')
    
    for pajama in pajama_sets:
        try:
            print(f'Updating: {pajama.name} (ID: {pajama.id}) - Brand: {pajama.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                nightsuit_url,
                folder='products',
                public_id=f'product_{pajama.id}_pajama_set_nightsuit',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=pajama).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=pajama,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_pajama_set()

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

def update_silk_ties():
    """Update all silk tie products with the specific Neiman Marcus image"""
    
    # Use the specific Neiman Marcus image URL provided
    neiman_marcus_url = 'https://media.neimanmarcus.com/f_auto,q_auto/01/nm_4489966_100551_m'
    
    # Find all silk tie products
    silk_ties = Product.objects.filter(name__icontains='silk tie')
    
    print(f'=== UPDATING {silk_ties.count()} SILK TIE PRODUCTS ===')
    
    for tie in silk_ties:
        try:
            print(f'Updating: {tie.name} (ID: {tie.id}) - Brand: {tie.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                neiman_marcus_url,
                folder='products',
                public_id=f'product_{tie.id}_silk_tie_neiman_marcus',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=tie).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=tie,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_silk_ties()

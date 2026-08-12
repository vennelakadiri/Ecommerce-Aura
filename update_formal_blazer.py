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

def update_formal_blazer():
    """Update all formal blazer products with the specific Louis Philippe image"""
    
    # Use the specific Louis Philippe image URL provided
    louis_philippe_url = 'https://imagescdn.louisphilippe.com/img/app/product/3/39687978-14048162.jpg'
    
    # Find all formal blazer products
    formal_blazers = Product.objects.filter(name__icontains='formal blazer')
    
    print(f'=== UPDATING {formal_blazers.count()} FORMAL BLAZER PRODUCTS ===')
    
    for blazer in formal_blazers:
        try:
            print(f'Updating: {blazer.name} (ID: {blazer.id}) - Brand: {blazer.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                louis_philippe_url,
                folder='products',
                public_id=f'product_{blazer.id}_formal_blazer_louis_philippe',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=blazer).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=blazer,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_formal_blazer()

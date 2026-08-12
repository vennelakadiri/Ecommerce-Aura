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

def update_slim_fit_jeans():
    """Update all slim fit jeans products with the specific Louis Philippe image"""
    
    # Use the specific Louis Philippe image URL provided
    louis_philippe_jeans_url = 'https://imagescdn.louisphilippe.com/img/app/product/4/40077201-21886843.jpg?auto=format&w=390'
    
    # Find all slim fit jeans products
    slim_fit_jeans = Product.objects.filter(name__icontains='slim fit jeans')
    
    print(f'=== UPDATING {slim_fit_jeans.count()} SLIM FIT JEANS PRODUCTS ===')
    
    for jeans in slim_fit_jeans:
        try:
            print(f'Updating: {jeans.name} (ID: {jeans.id}) - Brand: {jeans.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                louis_philippe_jeans_url,
                folder='products',
                public_id=f'product_{jeans.id}_slim_fit_jeans_louis_philippe',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=jeans).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=jeans,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_slim_fit_jeans()

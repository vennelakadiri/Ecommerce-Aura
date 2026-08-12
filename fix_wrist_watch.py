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

def fix_wrist_watch_image():
    """Fix the wrist watch product with proper image"""
    
    # Get the wrist watch product
    watch = Product.objects.get(id=1316)
    print(f'Updating: {watch.name} ({watch.brand.name})')
    
    # Use the perfect casio watch image (working URL)
    image_url = 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop&bg=white'
    
    # Upload to Cloudinary
    result = cloudinary.uploader.upload(
        image_url,
        folder='products',
        public_id='product_1316_wrist_watch',
        overwrite=True
    )
    
    # Remove existing images (if any)
    ProductImage.objects.filter(product=watch).delete()
    
    # Create new product image
    product_image = ProductImage.objects.create(
        product=watch,
        image=result['public_id'],
        is_primary=True
    )
    
    print(f'Updated with image: {result["secure_url"]}')
    print('Success!')

if __name__ == "__main__":
    fix_wrist_watch_image()

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

def update_yoga_pants():
    """Update all yoga pants products with the specific PrettyLittleThing image"""
    
    # Use the specific PrettyLittleThing image URL provided
    pretty_little_thing_url = 'https://cdn-img.prettylittlething.com/f/c/d/b/fcdb73b680066d5e235a4d9cdec973e3d18e6797_CNF7400_1_bone_ultimate_sculpt_flare_yoga_pants.jpg?imwidth=600'
    
    # Find all yoga pants products
    yoga_pants = Product.objects.filter(name__icontains='yoga pants')
    
    print(f'=== UPDATING {yoga_pants.count()} YOGA PANTS PRODUCTS ===')
    
    for pants in yoga_pants:
        try:
            print(f'Updating: {pants.name} (ID: {pants.id}) - Brand: {pants.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                pretty_little_thing_url,
                folder='products',
                public_id=f'product_{pants.id}_yoga_pants_pretty_little_thing',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=pants).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=pants,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_yoga_pants()

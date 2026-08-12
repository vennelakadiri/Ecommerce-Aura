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

def update_school_uniform():
    """Update all school uniform products with the specific Freepik image"""
    
    # Use the specific Freepik image URL provided
    freepik_url = 'https://img.freepik.com/free-photo/portrait-young-girl-student-school-uniform_23-2150282547.jpg?semt=ais_hybrid&w=740&q=80'
    
    # Find all school uniform products
    school_uniforms = Product.objects.filter(name__icontains='school uniform')
    
    print(f'=== UPDATING {school_uniforms.count()} SCHOOL UNIFORM PRODUCTS ===')
    
    for uniform in school_uniforms:
        try:
            print(f'Updating: {uniform.name} (ID: {uniform.id}) - Brand: {uniform.brand.name}')
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                freepik_url,
                folder='products',
                public_id=f'product_{uniform.id}_school_uniform_freepik',
                overwrite=True
            )
            
            # Remove existing images
            ProductImage.objects.filter(product=uniform).delete()
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=uniform,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f'  SUCCESS: {result["secure_url"]}')
            
        except Exception as e:
            print(f'  ERROR: {str(e)}')
    
    print('=== COMPLETED ===')

if __name__ == "__main__":
    update_school_uniform()

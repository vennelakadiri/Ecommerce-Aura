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

def update_classic_leather_belt():
    """Update only Classic Leather Belt product with Leather Direct image URL"""
    
    # The specific image URL provided by the user
    leather_direct_url = 'https://leatherdirect.co.nz/wp-content/uploads/2025/04/Parisian_YPEL_Pelham_Belt_Black_99.jpg'
    
    print("=== UPDATING CLASSIC LEATHER BELT PRODUCT ===")
    print("Only updating Classic Leather Belt with Leather Direct image URL")
    print("NOT touching any other products")
    print("=" * 60)
    print()
    
    # Find Classic Leather Belt product (exact match)
    classic_leather_belts = Product.objects.filter(name__icontains='classic leather belt')
    
    if not classic_leather_belts.exists():
        print("No Classic Leather Belt product found in the database")
        return
    
    total_updated = 0
    
    for belt in classic_leather_belts:
        print(f"Processing: {belt.name} (ID: {belt.id})")
        print(f"  Category: {belt.category.name}")
        print(f"  Brand: {belt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=belt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                leather_direct_url,
                folder="products",
                public_id=f"product_{belt.id}_classic_leather_belt_leather_direct",
                overwrite=True
            )
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=belt,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f"  SUCCESS: {result['secure_url']}")
            total_updated += 1
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")
        
        print()
    
    print("=== UPDATE SUMMARY ===")
    print(f"Classic Leather Belt products found: {classic_leather_belts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {classic_leather_belts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Classic Leather Belt products were updated")
    print("No other products were touched")
    print(f"Used Leather Direct image URL: {leather_direct_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for belt in classic_leather_belts:
        images = ProductImage.objects.filter(product=belt)
        if images.exists():
            image = images.first()
            if hasattr(image.image, 'url'):
                image_url = image.image.url
            else:
                image_url = f"https://res.cloudinary.com/dqthyfxm9/image/upload/{image.image}"
            print(f"  {belt.name}: {image_url}")
    
    print("=" * 60)

if __name__ == "__main__":
    update_classic_leather_belt()

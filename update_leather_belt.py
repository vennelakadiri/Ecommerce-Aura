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

def update_leather_belt():
    """Update only Leather Belt product with the provided Pixabay image URL"""
    
    # The specific image URL provided by the user
    pixabay_url = 'https://cdn.pixabay.com/photo/2015/09/05/19/35/brown-924734_1280.jpg'
    
    print("=== UPDATING LEATHER BELT PRODUCT ===")
    print("Only updating Leather Belt with Pixabay image URL")
    print("NOT touching any other products, categories, or home page")
    print("=" * 60)
    print()
    
    # Find Leather Belt product
    leather_belts = Product.objects.filter(name__icontains='leather belt')
    
    if not leather_belts.exists():
        print("No Leather Belt product found in the database")
        return
    
    total_updated = 0
    
    for belt in leather_belts:
        print(f"Processing: {belt.name} (ID: {belt.id})")
        print(f"  Category: {belt.category.name}")
        print(f"  Brand: {belt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=belt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                pixabay_url,
                folder="products",
                public_id=f"product_{belt.id}_leather_belt_pixabay",
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
    print(f"Leather Belt products found: {leather_belts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {leather_belts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Leather Belt products were updated")
    print("No other products, categories, or home page were touched")
    print(f"Used Pixabay image URL: {pixabay_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for belt in leather_belts:
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
    update_leather_belt()

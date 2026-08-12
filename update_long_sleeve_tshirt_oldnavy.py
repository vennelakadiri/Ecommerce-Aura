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

def update_long_sleeve_tshirt():
    """Update only Long Sleeve T-Shirt product with Old Navy Gap image URL"""
    
    # The specific image URL provided by the user
    oldnavy_url = 'https://oldnavy.gap.com/webcontent/0056/147/895/cn56147895.jpg'
    
    print("=== UPDATING LONG SLEEVE T-SHIRT PRODUCT ===")
    print("Only updating Long Sleeve T-Shirt with Old Navy Gap image URL")
    print("NOT touching any other products")
    print("=" * 60)
    print()
    
    # Find Long Sleeve T-Shirt products
    long_sleeve_tshirts = Product.objects.filter(name__icontains='long sleeve t-shirt')
    
    if not long_sleeve_tshirts.exists():
        print("No Long Sleeve T-Shirt product found in the database")
        return
    
    total_updated = 0
    
    for shirt in long_sleeve_tshirts:
        print(f"Processing: {shirt.name} (ID: {shirt.id})")
        print(f"  Category: {shirt.category.name}")
        print(f"  Brand: {shirt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=shirt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                oldnavy_url,
                folder="products",
                public_id=f"product_{shirt.id}_long_sleeve_tshirt_oldnavy",
                overwrite=True
            )
            
            # Create new product image
            product_image = ProductImage.objects.create(
                product=shirt,
                image=result['public_id'],
                is_primary=True
            )
            
            print(f"  SUCCESS: {result['secure_url']}")
            total_updated += 1
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")
        
        print()
    
    print("=== UPDATE SUMMARY ===")
    print(f"Long Sleeve T-Shirt products found: {long_sleeve_tshirts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {long_sleeve_tshirts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Long Sleeve T-Shirt products were updated")
    print("No other products were touched")
    print(f"Used Old Navy Gap image URL: {oldnavy_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for shirt in long_sleeve_tshirts:
        images = ProductImage.objects.filter(product=shirt)
        if images.exists():
            image = images.first()
            if hasattr(image.image, 'url'):
                image_url = image.image.url
            else:
                image_url = f"https://res.cloudinary.com/dqthyfxm9/image/upload/{image.image}"
            print(f"  {shirt.name}: {image_url}")
    
    print("=" * 60)

if __name__ == "__main__":
    update_long_sleeve_tshirt()

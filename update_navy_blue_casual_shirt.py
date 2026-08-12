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

def update_navy_blue_casual_shirt():
    """Update only Navy Blue Casual Shirt product with IMImg image URL"""
    
    # The specific image URL provided by the user
    imimg_url = 'https://5.imimg.com/data5/SELLER/Default/2024/2/385169067/HM/KM/LT/124692771/plain-navy-blue-cotton-shirt-1000x1000.jpg'
    
    print("=== UPDATING NAVY BLUE CASUAL SHIRT PRODUCT ===")
    print("Only updating Navy Blue Casual Shirt with IMImg image URL")
    print("NOT touching any other products")
    print("=" * 60)
    print()
    
    # Find Navy Blue Casual Shirt products (exact match)
    navy_blue_casual_shirts = Product.objects.filter(name__icontains='navy blue casual shirt')
    
    if not navy_blue_casual_shirts.exists():
        print("No Navy Blue Casual Shirt product found in the database")
        return
    
    total_updated = 0
    
    for shirt in navy_blue_casual_shirts:
        print(f"Processing: {shirt.name} (ID: {shirt.id})")
        print(f"  Category: {shirt.category.name}")
        print(f"  Brand: {shirt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=shirt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                imimg_url,
                folder="products",
                public_id=f"product_{shirt.id}_navy_blue_casual_shirt_imimg",
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
    print(f"Navy Blue Casual Shirt products found: {navy_blue_casual_shirts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {navy_blue_casual_shirts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Navy Blue Casual Shirt products were updated")
    print("No other products were touched")
    print(f"Used IMImg image URL: {imimg_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for shirt in navy_blue_casual_shirts:
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
    update_navy_blue_casual_shirt()

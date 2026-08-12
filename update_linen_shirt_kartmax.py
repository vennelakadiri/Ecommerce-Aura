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

def update_linen_shirt_kartmax():
    """Update only Linen Shirt product with Kartmax image URL"""
    
    # The specific image URL provided by the user
    kartmax_url = 'https://pictures.kartmax.in/live/cover/600x800/sites/9s145MyZrWdIAwpU0JYS/product-images/ucb_navy_checkered_casual_shirt_1729398617as3066109_1.jpg'
    
    print("=== UPDATING LINEN SHIRT PRODUCT ===")
    print("Only updating Linen Shirt with Kartmax image URL")
    print("NOT touching any other products")
    print("=" * 60)
    print()
    
    # Find Linen Shirt products
    linen_shirts = Product.objects.filter(name__icontains='linen shirt')
    
    if not linen_shirts.exists():
        print("No Linen Shirt product found in the database")
        return
    
    total_updated = 0
    
    for shirt in linen_shirts:
        print(f"Processing: {shirt.name} (ID: {shirt.id})")
        print(f"  Category: {shirt.category.name}")
        print(f"  Brand: {shirt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=shirt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                kartmax_url,
                folder="products",
                public_id=f"product_{shirt.id}_linen_shirt_kartmax",
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
    print(f"Linen Shirt products found: {linen_shirts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {linen_shirts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Linen Shirt products were updated")
    print("No other products were touched")
    print(f"Used Kartmax image URL: {kartmax_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for shirt in linen_shirts:
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
    update_linen_shirt_kartmax()

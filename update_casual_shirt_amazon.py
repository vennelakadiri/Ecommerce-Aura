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

def update_casual_shirt():
    """Update only Casual Shirt product with Amazon image URL"""
    
    # The specific image URL provided by the user
    amazon_url = 'https://m.media-amazon.com/images/I/71sYkdV+D7L._UL1500_.jpg'
    
    print("=== UPDATING CASUAL SHIRT PRODUCT ===")
    print("Only updating Casual Shirt with Amazon image URL")
    print("NOT touching any other products")
    print("=" * 60)
    print()
    
    # Find Casual Shirt products
    casual_shirts = Product.objects.filter(name__icontains='casual shirt')
    
    if not casual_shirts.exists():
        print("No Casual Shirt product found in the database")
        return
    
    total_updated = 0
    
    for shirt in casual_shirts:
        print(f"Processing: {shirt.name} (ID: {shirt.id})")
        print(f"  Category: {shirt.category.name}")
        print(f"  Brand: {shirt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=shirt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                amazon_url,
                folder="products",
                public_id=f"product_{shirt.id}_casual_shirt_amazon",
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
    print(f"Casual Shirt products found: {casual_shirts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {casual_shirts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Casual Shirt products were updated")
    print("No other products were touched")
    print(f"Used Amazon image URL: {amazon_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for shirt in casual_shirts:
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
    update_casual_shirt()

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

def update_polo_style_tshirt():
    """Update only Polo Style T-Shirt product with Clothcraft image URL"""
    
    # The specific image URL provided by the user
    clothcraft_url = 'https://theclothcraft.com/wp-content/uploads/2023/10/3-4.jpg'
    
    print("=== UPDATING POLO STYLE T-SHIRT PRODUCT ===")
    print("Only updating Polo Style T-Shirt with Clothcraft image URL")
    print("NOT touching any other products")
    print("=" * 60)
    print()
    
    # Find Polo Style T-Shirt products
    polo_style_tshirts = Product.objects.filter(name__icontains='polo style t-shirt')
    
    if not polo_style_tshirts.exists():
        print("No Polo Style T-Shirt product found in the database")
        return
    
    total_updated = 0
    
    for shirt in polo_style_tshirts:
        print(f"Processing: {shirt.name} (ID: {shirt.id})")
        print(f"  Category: {shirt.category.name}")
        print(f"  Brand: {shirt.brand.name}")
        
        try:
            # Remove existing images
            ProductImage.objects.filter(product=shirt).delete()
            print(f"  Removed existing images")
            
            # Upload new image to Cloudinary
            result = cloudinary.uploader.upload(
                clothcraft_url,
                folder="products",
                public_id=f"product_{shirt.id}_polo_style_tshirt_clothcraft",
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
    print(f"Polo Style T-Shirt products found: {polo_style_tshirts.count()}")
    print(f"Successfully updated: {total_updated}")
    print(f"Failed updates: {polo_style_tshirts.count() - total_updated}")
    
    print("\n=== VERIFICATION ===")
    print("Only Polo Style T-Shirt products were updated")
    print("No other products were touched")
    print(f"Used Clothcraft image URL: {clothcraft_url}")
    
    print("\n=== UPDATED PRODUCTS ===")
    for shirt in polo_style_tshirts:
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
    update_polo_style_tshirt()
